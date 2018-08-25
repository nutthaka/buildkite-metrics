# buildkite-metrics

Experimenting to collect data from Buildkite pipelines

## Run
Scripts require configuration values. You need to provide config values in a file or pass the values as ENV variables.

For a config file, source the file.

    source config.env

    ./pipelines_count.py > builds.csv