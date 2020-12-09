# Changelog

## [1.9.0](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.9.0) (2020-12-09)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.8.1...1.9.0)

**Implemented enhancements:**

- improve support for API parameters [\#66](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/66) ([schurzi](https://github.com/schurzi))
- Notification templates [\#64](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/64) ([rndmh3ro](https://github.com/rndmh3ro))

**Closed issues:**

- icinga\_commands with "imports" not working [\#63](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/issues/63)
- Can't use fields available in API - e.g. host\_template - has\_agent [\#59](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/issues/59)

## [1.8.1](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.8.1) (2020-11-05)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.8.0...1.8.1)

**Implemented enhancements:**

- Unsupported parameter "Notes" for icinga\_host [\#50](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/issues/50)
- added vsc code snippets [\#57](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/57) ([xFuture603](https://github.com/xFuture603))

## [1.8.0](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.8.0) (2020-10-28)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.7.1...1.8.0)

**Implemented enhancements:**

- Add support for notes and notes\_url to all relevant objects [\#56](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/56) ([mmslkr](https://github.com/mmslkr))

## [1.7.1](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.7.1) (2020-10-26)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.7.0...1.7.1)

**Fixed bugs:**

- Icinga Object "Service" rerun - failed to recreate if object\_name contains spaces [\#52](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/issues/52)
- allow using whitespaces in object names [\#55](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/55) ([schurzi](https://github.com/schurzi))

**Merged pull requests:**

- improve coverage of new service module [\#51](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/51) ([rndmh3ro](https://github.com/rndmh3ro))

## [1.7.0](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.7.0) (2020-10-23)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.6.0...1.7.0)

**Implemented enhancements:**

- update examples and tests so they can actually be deployed [\#54](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/54) ([rndmh3ro](https://github.com/rndmh3ro))
- add check\_command arg to service\_apply module [\#53](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/53) ([rndmh3ro](https://github.com/rndmh3ro))

**Closed issues:**

- Add object "Service" for a Host [\#42](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/issues/42)

**Merged pull requests:**

- add example and test for command without args [\#46](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/46) ([rndmh3ro](https://github.com/rndmh3ro))

## [1.6.0](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.6.0) (2020-10-22)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.5.0...1.6.0)

**Implemented enhancements:**

- add new service module [\#32](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/32) ([rndmh3ro](https://github.com/rndmh3ro))

## [1.5.0](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.5.0) (2020-10-02)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.4.3...1.5.0)

**Implemented enhancements:**

- Add Support for Zones and Endpoints [\#48](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/48) ([arbu](https://github.com/arbu))
- Create codeql-analysis.yml [\#47](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/47) ([rndmh3ro](https://github.com/rndmh3ro))

## [1.4.3](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.4.3) (2020-10-01)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.4.2...1.4.3)

**Fixed bugs:**

- Hosts in state absent don't require import parameter [\#44](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/issues/44)
- when deleting objects, only the object\_name is required  [\#45](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/45) ([rndmh3ro](https://github.com/rndmh3ro))

## [1.4.2](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.4.2) (2020-09-25)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.4.1...1.4.2)

**Implemented enhancements:**

- add timeout parameter to icinga\_command.yml [\#43](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/43) ([AnBenn](https://github.com/AnBenn))

## [1.4.1](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.4.1) (2020-09-02)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.4.0...1.4.1)

**Implemented enhancements:**

- make local testing without ansible-test work [\#41](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/41) ([rndmh3ro](https://github.com/rndmh3ro))
- Add more Integrationtests [\#39](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/39) ([rndmh3ro](https://github.com/rndmh3ro))
- Testing update [\#38](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/38) ([rndmh3ro](https://github.com/rndmh3ro))

**Fixed bugs:**

- No IPv6-Address Variable for Hosts [\#36](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/issues/36)

**Merged pull requests:**

- add badge to readme [\#40](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/40) ([rndmh3ro](https://github.com/rndmh3ro))

## [1.4.0](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.4.0) (2020-08-04)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.3.2...1.4.0)

**Implemented enhancements:**

- add support for address6 on host object [\#37](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/37) ([schurzi](https://github.com/schurzi))

## [1.3.2](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.3.2) (2020-07-15)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.3.1...1.3.2)

**Implemented enhancements:**

- make local testing without ansible-test easier [\#33](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/33) ([rndmh3ro](https://github.com/rndmh3ro))

**Fixed bugs:**

- added code in icinga\_command.yml to make it work like the other tasks in our role [\#35](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/35) ([xFuture603](https://github.com/xFuture603))

**Merged pull requests:**

- update examples and bash script for new testing paths [\#31](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/31) ([rndmh3ro](https://github.com/rndmh3ro))

## [1.3.1](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.3.1) (2020-07-07)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.3.0...1.3.1)

**Merged pull requests:**

- replace hyphen in role name with underscore [\#29](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/29) ([rndmh3ro](https://github.com/rndmh3ro))

## [1.3.0](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.3.0) (2020-07-07)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.2.2...1.3.0)

**Implemented enhancements:**

- Ansible icinga role [\#28](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/28) ([michaelamattes](https://github.com/michaelamattes))

## [1.2.2](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.2.2) (2020-06-26)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.2.1...1.2.2)

**Implemented enhancements:**

- Use ansible-test to run integration tests [\#27](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/27) ([rndmh3ro](https://github.com/rndmh3ro))

**Fixed bugs:**

- zone: defaults to master but i do not want to configure zone at all. [\#25](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/issues/25)

**Merged pull requests:**

- do not set zone to master in host and hosttemplate [\#26](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/26) ([rndmh3ro](https://github.com/rndmh3ro))

## [1.2.1](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.2.1) (2020-06-25)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.2.0...1.2.1)

**Implemented enhancements:**

- Integration testing [\#24](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/24) ([rndmh3ro](https://github.com/rndmh3ro))
- Add proper linting [\#22](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/22) ([rndmh3ro](https://github.com/rndmh3ro))

## [1.2.0](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.2.0) (2020-06-24)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.1.4...1.2.0)

**Implemented enhancements:**

- add gitattributes because of windows line endings [\#21](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/21) ([rndmh3ro](https://github.com/rndmh3ro))
- add icinga\_host\_template [\#20](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/20) ([michaelamattes](https://github.com/michaelamattes))
- add troubleshooting section [\#19](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/19) ([rndmh3ro](https://github.com/rndmh3ro))

**Fixed bugs:**

- do not require import and check\_command in host\_template [\#23](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/23) ([rndmh3ro](https://github.com/rndmh3ro))

**Closed issues:**

- Error creating servicegroups [\#13](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/issues/13)

## [1.1.4](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.1.4) (2020-06-12)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.1.3...1.1.4)

**Implemented enhancements:**

- further improve error messages for different errors [\#18](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/18) ([rndmh3ro](https://github.com/rndmh3ro))
- added required ansible version to readme.md [\#17](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/17) ([xFuture603](https://github.com/xFuture603))

## [1.1.3](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.1.3) (2020-06-09)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.1.2...1.1.3)

**Implemented enhancements:**

- try to improve error messages [\#16](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/16) ([rndmh3ro](https://github.com/rndmh3ro))
- add steps to update galaxy.yml in publish action [\#15](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/15) ([rndmh3ro](https://github.com/rndmh3ro))

## [1.1.2](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.1.2) (2020-06-09)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.1.1...1.1.2)

**Implemented enhancements:**

- add action to publish to galaxy [\#14](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/14) ([rndmh3ro](https://github.com/rndmh3ro))
- github-action to automatically create release-drafts [\#12](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/12) ([rndmh3ro](https://github.com/rndmh3ro))
- remove unused intermediate assignments [\#11](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/11) ([schurzi](https://github.com/schurzi))

**Fixed bugs:**

- assign\_filter variable in icinga\_notification module should be a string [\#9](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/issues/9)

## [1.1.1](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.1.1) (2020-06-04)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.1.0...1.1.1)

**Implemented enhancements:**

- fix issue \#9 - define assing\_filter as string [\#10](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/10) ([FLiPp3r90](https://github.com/FLiPp3r90))

## [1.1.0](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.1.0) (2020-05-25)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/1.0.0...1.1.0)

**Implemented enhancements:**

- Add icinga command template [\#8](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/8) ([mmslkr](https://github.com/mmslkr))

**Fixed bugs:**

- fix name of imports [\#7](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/7) ([rndmh3ro](https://github.com/rndmh3ro))

## [1.0.0](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/tree/1.0.0) (2020-05-15)

[Full Changelog](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/compare/2492296965515a9ac885c6a4874acba8a7475895...1.0.0)

**Merged pull requests:**

- update urls, lowercase name [\#6](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/6) ([rndmh3ro](https://github.com/rndmh3ro))
- replace - with \_ [\#5](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/5) ([rndmh3ro](https://github.com/rndmh3ro))
- alter readme to accomodate for collection [\#4](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/4) ([rndmh3ro](https://github.com/rndmh3ro))
- Linting fixes [\#3](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/3) ([rndmh3ro](https://github.com/rndmh3ro))
- Create main.yml [\#2](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/2) ([rndmh3ro](https://github.com/rndmh3ro))
- Create ansible-lint.yml [\#1](https://github.com/T-Systems-MMS/ansible-collection-icinga-director/pull/1) ([rndmh3ro](https://github.com/rndmh3ro))



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*
