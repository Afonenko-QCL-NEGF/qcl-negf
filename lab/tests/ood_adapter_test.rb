# frozen_string_literal: true

require 'minitest/autorun'
require 'tmpdir'

core_root = File.expand_path(ENV.fetch('OODCORE_ROOT'))
raise ArgumentError, 'OODCORE_ROOT must contain the ood_core source' unless File.file?(File.join(core_root, 'lib/ood_core/job/adapters/htcondor.rb'))
$LOAD_PATH.unshift(File.join(core_root, 'lib'))
require 'ood_core/errors'
require 'ood_core/refinements/array_extensions'
require 'ood_core/job/adapter'
require 'ood_core/job/script'
require 'ood_core/job/status'
require 'ood_core/job/info'
require 'ood_core/job/adapters/htcondor'

# Проверяет границу OOD Script → native command, не отправляя задания.
class OodAdapterTest < Minitest::Test
  class RecordingBatch < OodCore::Job::Adapters::HTCondor::Batch
    attr_reader :submission, :calls

    def initialize
      @default_universe = 'vanilla'
      @default_docker_image = 'unused'
      @additional_attributes = {}
      @submit_host = ''
      @calls = []
    end

    def submit_string(**options)
      @submission = options
      '123'
    end

    def call(command, *args, **options)
      @calls << [command, args, options]
      return '' unless command == 'condor_q'

      record = {
        'ClusterId' => '123', 'ProcId' => '0', 'JobStatus' => '2',
        'Owner' => 'testuser', 'JobBatchName' => 'GUI job with spaces',
        'CpusProvisioned' => '2', 'GpusProvisioned' => '0',
        'QDate' => '1700000000', 'JobCurrentStartDate' => '1700000001',
        'RemoteSysCpu' => '1.5', 'RemoteUserCpu' => '2.5',
        'RemoteWallClockTime' => '3', 'RequestCpus' => '2',
        'RequestMemory' => '768'
      }
      condor_q_attrs.values.map { |field| record.fetch(field, 'undefined') }.join("\t") + "\n"
    end
  end

  def setup
    @batch = RecordingBatch.new
    @adapter = OodCore::Job::Adapters::HTCondor.new(htcondor: @batch)
  end

  def appended_values
    @batch.submission.fetch(:args).each_cons(2).filter_map do |key, value|
      value if key == '-a'
    end
  end

  def test_job_composer_can_submit_default_nil_resources
    assert_equal '123', @adapter.submit(OodCore::Job::Script.new(content: 'echo test'))
    assert_includes appended_values, 'request_cpus=1'
    assert_includes appended_values, 'request_memory=1024'
  end

  def test_project_launcher_preserves_explicit_resources_and_input_files
    native = { 'request_memory' => 768, 'transfer_input_files' => 'input.txt', '+ContractProbe' => 'true' }.freeze
    script = OodCore::Job::Script.new(content: 'cat input.txt', cores: 2, native: native)

    assert_equal '123', @adapter.submit(script, after: [], afterok: [], afternotok: [], afterany: [])
    assert_includes appended_values, 'request_cpus=2'
    assert_includes appended_values, 'request_memory=768'
    refute_includes appended_values, 'request_memory=2048'
    assert_includes appended_values, '+ContractProbe=true'
    assert_equal 'input.txt', @batch.submission[:transfer_input_files]
    assert_equal native, script.native
  end

  def test_actual_dependencies_are_rejected_before_submission
    error = assert_raises(OodCore::JobAdapterError) do
      @adapter.submit(OodCore::Job::Script.new(content: 'echo test'), afterok: ['42'])
    end
    assert_match(/dependencies are not supported/, error.message)
    assert_nil @batch.submission
  end

  def test_status_preserves_native_names_and_cancel_uses_the_full_job_id
    info = @adapter.info('123.0')

    assert_equal '123.0', info.id
    assert_equal 'GUI job with spaces', info.job_name
    assert_equal :running, info.status.to_sym
    assert_kind_of Hash, info.native
    assert_equal 'GUI job with spaces', info.native['JobBatchName']
    assert_equal ['-constraint', 'ClusterId == 123 && ProcId == 0'], @batch.calls.last[1].first(2)

    @adapter.delete('123.0')
    assert_equal ['condor_rm', ['123.0'], {}], @batch.calls.last
  end

  def test_input_transfer_contains_the_script_and_only_explicit_inputs
    batch = OodCore::Job::Adapters::HTCondor::Batch.allocate
    calls = []
    batch.define_singleton_method(:call) do |command, *args, **options|
      calls << [command, args, options]
      command == 'condor_submit' ? '123.0 - 123.0' : ''
    end

    assert_equal '123', batch.submit_string(script: 'cat input.txt', transfer_input_files: 'input.txt')
    description = calls.last[2].fetch(:stdin)
    temporary_script = File.join(Dir.tmpdir, 'htcondor_submit_')
    assert_match(/transfer_input_files=#{Regexp.escape(temporary_script)}[^,\n]+,input\.txt\n/, description)
    assert_match(/arguments=htcondor_submit_/, description)
  end
end
