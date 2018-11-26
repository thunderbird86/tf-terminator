## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|:----:|:-----:|:-----:|
| name | - | string | `terminator` | no |
| run\_on\_regions | The list of AWS regions where to run the schedulers. | list | `[ "" ]` | no |
| scheduler\_interval | The interval of execution of the scheduler. | string | `rate(5 minutes)` | no |

