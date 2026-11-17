# frozen_string_literal: true

require 'minitest/autorun'
require 'tmpdir'
require 'active_support/all'
require 'active_model'
require 'action_dispatch'
require 'action_controller'
require 'action_view'
require 'erb'

core_root = File.expand_path(ENV.fetch('OODCORE_ROOT'))
dashboard_root = File.expand_path(ENV.fetch('OOD_DASHBOARD_ROOT'))
raise ArgumentError, 'OODCORE_ROOT must contain the ood_core source' unless File.file?(File.join(core_root, 'lib/ood_core/job/adapters/htcondor.rb'))
$LOAD_PATH.unshift(File.join(core_root, 'lib'))
require 'ood_core/errors'
require 'ood_core/refinements/array_extensions'
require 'ood_core/job/adapter'
require 'ood_core/job/script'
require 'ood_core/job/status'
require 'ood_core/job/info'
require 'ood_core/job/adapters/htcondor'

%w[
  app/models/concerns/bool_reader.rb
  app/models/concerns/icon_with_uri.rb
  app/models/concerns/project_permissions.rb
  app/models/concerns/job_logger.rb
  app/lib/smart_attributes/attribute.rb
  app/lib/smart_attributes/attributes/auto_cores.rb
  app/lib/smart_attributes/attributes/auto_memory.rb
  app/lib/smart_attributes/attributes/auto_input_files.rb
  app/models/hpc_job.rb
  app/helpers/projects_helper.rb
  app/models/project.rb
].each { |path| require File.join(dashboard_root, path) }

Object.const_set(:ProjectsController, Class.new(ActionController::Base)) unless defined?(ProjectsController)

# Настоящие модели, helpers, routes и ERB; scheduler и запись cache заменены.
# Rails application/PUN не загружается, заданий и app state tests не создают.
class JobDetailsTest < Minitest::Test
  DASHBOARD_ROOT = File.expand_path(ENV.fetch('OOD_DASHBOARD_ROOT'))

  class HistoryBatch < OodCore::Job::Adapters::HTCondor::Batch
    attr_accessor :history_status

    def initialize
      @submit_host = ''
      @history_status = '4'
    end

    def call(command, *_args, **_options)
      return '' if command == 'condor_q' || history_status.nil?
      raise "Unexpected command: #{command}" unless command == 'condor_history'

      record = {
        'ClusterId' => '6', 'ProcId' => '0', 'JobStatus' => history_status,
        'Owner' => 'testuser', 'CpusProvisioned' => '2', 'GpusProvisioned' => '0',
        'QDate' => '1700000000', 'JobCurrentStartDate' => '1700000001',
        'RemoteSysCpu' => '0.0', 'RemoteUserCpu' => '0.0',
        'RemoteWallClockTime' => '46.0', 'ExitCode' => '0',
        'ExitBySignal' => 'false', 'RequestCpus' => '2', 'RequestMemory' => '769',
        'RemoveReason' => 'via condor_rm (by user testuser)'
      }
      condor_q_attrs.values.map { |field| record.fetch(field, 'undefined') }.join("\t") + "\n"
    end
  end

  class View
    include ProjectsHelper

    def status_class(status); status; end
    def status_text(status); status; end
    def job_details_buttons(*); ''; end
    def render(*); '<div>native details</div>'; end

    def render_source(source, job, project = nil)
      ERB.new(source, trim_mode: '-').result(binding)
    end
  end

  def setup
    @batch = HistoryBatch.new
    @adapter = OodCore::Job::Adapters::HTCondor.new(htcondor: @batch)
  end

  def template(name)
    File.read(File.join(DASHBOARD_ROOT, "app/views/projects/_job_details#{name}.erb"))
  end

  def project_with_cached_jobs(cached_jobs)
    project = Project.allocate
    project.instance_variable_set(:@directory, Pathname.new(Dir.tmpdir).join('ood-contract-fixture'))
    project.define_singleton_method(:jobs) { cached_jobs }
    adapter = @adapter
    project.define_singleton_method(:adapter) { |_cluster| adapter }
    project
  end

  def test_terminal_history_has_native_state_and_exit_status
    job = @adapter.info('6.0')

    assert_equal :completed, job.status.to_sym
    assert_kind_of Hash, job.native
    assert_equal 'COMPLETED', job.native[:state]
    assert_equal 'exit code 0', job.native[:reason]
    assert_equal '769', job.native['RequestMemory']

    @batch.history_status = '3'
    removed = @adapter.info('6.0')
    assert_equal 'REMOVED', removed.native[:state]
    assert_match(/condor_rm/, removed.native[:reason])
  end

  def test_native_form_producer_keeps_cpu_memory_and_explicit_inputs
    memory = SmartAttributes::Attributes::AutoMemory.new('auto_memory', value: '896')
    attributes = [
      SmartAttributes::Attributes::AutoCores.new('auto_cores', value: '3'),
      memory,
      SmartAttributes::Attributes::AutoInputFiles.new('auto_input_files', value: 'input.txt')
    ]
    options = attributes.map { |attribute| attribute.submit(fmt: 'htcondor') }.reduce(&:deep_merge).fetch(:script)
    script = OodCore::Job::Script.new(content: 'cat input.txt', **options)

    assert_equal 3, script.cores
    assert_equal 896, script.native[:request_memory]
    assert_equal 'input.txt', script.native[:transfer_input_files]
    assert_raises(ArgumentError) { memory.submit(fmt: 'unsupported') }
  end

  def test_missing_queue_and_history_is_unknown
    @batch.history_status = nil
    info = @adapter.info('999999.0')

    assert_equal :undetermined, info.status.to_sym
    assert_equal 'UNKNOWN', info.native[:state]
    assert_nil View.new.button_category(info.status.to_s)
  end

  def test_project_routes_keep_native_dot_ids
    # Эти три route definitions взяты из проверяемого source без копирования regex.
    fragment = File.readlines(File.join(DASHBOARD_ROOT, 'config/routes.rb'))
                   .grep(%r{/jobs/:cluster/:jobid}).join
    routes = ActionDispatch::Routing::RouteSet.new
    routes.draw do
      resources :projects do
        instance_eval(fragment)
      end
    end

    [[:get, '/6.0'], [:delete, '/6.0'], [:post, '/6.0/stop']].each do |method, suffix|
      recognized = routes.recognize_path('/projects/testproject/jobs/testcluster' + suffix, method: method)
      assert_equal '6.0', recognized[:jobid]
    end
    assert_equal 'turbo_stream', routes.recognize_path('/projects/testproject/jobs/testcluster/6.0')[:format]
  end

  def test_project_fetches_a_missing_cache_entry
    project = project_with_cached_jobs([])
    upserts = []
    Project.stub(:upsert_job!, ->(_directory, job) { upserts << job }) do
      assert_equal '6.0', project.job('6.0', 'testcluster').id
    end
    assert_equal 1, upserts.length
  end

  def test_legacy_completed_cache_must_refetch_native_history
    [nil, ['6', '0']].each do |legacy_native|
      cached = HpcJob.new(id: '6.0', status: 'completed', cluster: 'testcluster', native: legacy_native)
      assert_equal 'UNKNOWN', cached.native[:state]
      project = project_with_cached_jobs([cached])

      Project.stub(:upsert_job!, ->(*) {}) do
        @batch.history_status = nil
        missing = project.job('6.0', 'testcluster')
        assert_equal :undetermined, missing.status.to_sym
        assert_equal 'UNKNOWN', missing.native[:state]

        @batch.history_status = '4'
        terminal = project.job('6.0', 'testcluster')
        assert_equal 'COMPLETED', terminal.native[:state]
        assert_equal 'exit code 0', terminal.native[:reason]
      end
    end
  end

  def test_human_display_accepts_rails_date_helper_and_missing_time
    job = HpcJob.from_core_info(info: @adapter.info('6.0'), cluster: 'testcluster')
    display = job.to_human_display

    assert_kind_of String, display['Wallclock time']
    refute display.key?('Wallclock limit')

    legacy = HpcJob.new(id: '6.0', status: 'queued', cluster: 'testcluster', native: ['6', '0'])
    assert_equal ['6', '0'], legacy.native[:raw]
    assert_kind_of String, View.new.native_message(legacy.native)
  end

  def test_turbo_and_collapse_ids_are_css_safe_and_preserve_native_job_id
    job = HpcJob.from_core_info(info: @adapter.info('6.0'), cluster: 'testcluster')
    view = View.new
    placeholder = view.render_source(template('.html'), job)
    turbo = view.render_source(template('.turbo_stream'), job)
    content = view.render_source(template('_content.html'), job)
    dom_id = placeholder[/\bid="([^"]+)"/, 1]

    assert_match(/\A[a-zA-Z_][a-zA-Z0-9_-]*\z/, dom_id)
    assert_includes placeholder, 'data-job-id="6.0"'
    assert_includes turbo, "target=\"#{dom_id}\""
    assert_includes content, "id=\"#{dom_id}_data\""
    assert_includes content, "data-bs-target=\"##{dom_id}_data\""
  end
end
