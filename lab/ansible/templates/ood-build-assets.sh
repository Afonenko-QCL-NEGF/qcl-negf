#!/bin/bash
# Native OOD asset pipeline; dependencies must already be installed.
set -euo pipefail
cd /var/www/ood/apps/sys/dashboard
export GEM_PATH="/opt/ood/gems:$(ruby -e 'puts Gem.path.join(":")')"
export GEM_HOME=/opt/ood/gems
export BUNDLE_WITHOUT=development:test:doc
export RAILS_ENV=production
export RAILS_RELATIVE_URL_ROOT=/pun/sys/dashboard
export SECRET_KEY_BASE_DUMMY=1
export SKIP_JS_BUILD=1 SKIP_CSS_BUILD=1
# Reuse package dependencies; do not invoke an install during compilation.
test -x node_modules/.bin/esbuild
test -r node_modules/sass/sass.js
npm run build
node node_modules/sass/sass.js ./app/assets/stylesheets/application.scss ./app/assets/builds/application.css --load-path=node_modules
# Retain old assets for existing browser requests; no assets:clobber.
/opt/ood/gems/bin/bundle exec rake assets:precompile
