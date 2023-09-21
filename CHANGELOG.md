# CHANGELOG



## v2.1.0 (2023-09-21)

### Build

* build: changed semantic-release behavior ([`0ca54fc`](https://github.com/srv/git/chew/commit/0ca54fc0ff517f37c278e22e43a8f4b54174678c))

### Chore

* chore: merge branch &#39;main&#39; of origin ([`9e7b190`](https://github.com/srv/git/chew/commit/9e7b1909a20b6ed859671f227bbb7f862b7061a0))

### Feature

* feat: added new function for getting the consumed position

Added a new function at_pos for getting the exact location (both line
and character number) of the consumed input. ([`b303e22`](https://github.com/srv/git/chew/commit/b303e22488471f110759b37d34e5acec36caf009))

### Refactor

* refactor: created function for getting consumed input ([`453fed4`](https://github.com/srv/git/chew/commit/453fed426e79b0b479468c1fb3f9f9db94c8e31d))

* refactor: removed impossible branch from coverage testing ([`9d6f85e`](https://github.com/srv/git/chew/commit/9d6f85e8d16c935df02cd31754d2f56446e87abf))

### Test

* test: added test cases for error functionality ([`ad4d68a`](https://github.com/srv/git/chew/commit/ad4d68a9ebf435c3f84f7fc41ef45d12209314d8))

* test: added tests for new functionality ([`8839d6e`](https://github.com/srv/git/chew/commit/8839d6ea9257b43b15d0c732d7326f39359539a1))

* test: corrected tests to better reflect at_line functionality ([`433bc2d`](https://github.com/srv/git/chew/commit/433bc2dc00c8f7dfdd4b55322e64e25484877678))

* test: added test for using take on exhausted iterator ([`2aacffb`](https://github.com/srv/git/chew/commit/2aacffb8906808736c5c435bd7815f0c85f1fced))


## v2.0.1 (2023-09-20)

### Chore

* chore: modified project definition to include typedefs ([`19c5842`](https://github.com/srv/git/chew/commit/19c58429469b98b985b608a03dd90156e51ec522))


## v2.0.0 (2023-09-20)

### Breaking

* refactor!: refined ErrorKind variants and impl changes ([`10d8ca3`](https://github.com/srv/git/chew/commit/10d8ca37d59cad7ac415ace2c75b46697df3fc43))

* refactor!: changed is_a and is_not to fail on no match ([`380b1ca`](https://github.com/srv/git/chew/commit/380b1cad1ae73b05ede0ccbde81f463d0c1488bf))

* refactor!: added ErrorKind(s) to Error values ([`053d5f3`](https://github.com/srv/git/chew/commit/053d5f353e45227d579b4ba39b38eb9138aa28e1))

* refactor!: changed names of core types ([`ec8e72e`](https://github.com/srv/git/chew/commit/ec8e72e8150a036189f510674df134f533595cb9))

### Feature

* feat: added function for ignoring an ErrorKind to error module ([`b36b09f`](https://github.com/srv/git/chew/commit/b36b09fc5b9d8b4be4489b9e7af2944c6bb777a1))

* feat: added the ability to chain errors with origins ([`d819486`](https://github.com/srv/git/chew/commit/d81948675d6013b8de8de22ec74ed3e03929b4bc))

### Fix

* fix: fixed Exception type detection ([`7008a8c`](https://github.com/srv/git/chew/commit/7008a8c6fe351b4241fd2149e0835329ea092874))

* fix: fixed Exception type detection ([`318c407`](https://github.com/srv/git/chew/commit/318c40744eec8123e5716cbff5b3a7608ceeb287))

### Refactor

* refactor: changed naming scheme of variable in tag ([`e68c487`](https://github.com/srv/git/chew/commit/e68c48722d10ca5d80590b456c10669c05a3d39a))

* refactor: changed `map_res` error return semantics ([`4872961`](https://github.com/srv/git/chew/commit/48729615391e4750474768e8f97eaf4952b1974e))


## v1.0.0 (2023-09-20)


## v0.1.0 (2023-09-04)

### Chore

* chore: initial commit ([`a65bbd9`](https://github.com/srv/git/chew/commit/a65bbd939393361c532f4d2dca5b73df2ec089a9))
