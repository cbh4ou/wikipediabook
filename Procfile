web: gunicorn wikibook.wsgi --chdir backend --limit-request-line 8188 --log-file -
worker: REMAP_SIGTERM=SIGQUIT celery --workdir backend --app=wikibook worker --loglevel=info
beat: REMAP_SIGTERM=SIGQUIT celery --workdir backend --app=wikibook beat -S redbeat.RedBeatScheduler --loglevel=info
