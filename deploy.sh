#!/bin/bash

cdk synth

cdk deploy --require-approval=never "log-processor-infrastructure logging-datagen"
cdk deploy --require-approval=never --debug --no-rollback "stream-processor"
