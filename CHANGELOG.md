# CHANGELOG



## v3.1.0 (2023-09-24)

### Chore

* chore: updated dependencies ([`91eb8f3`](https://github.com/srv/git/chew/commit/91eb8f34b5bdc1bc9a6a4db01b6f74c9a1b3ba85))

* chore: added coverage.py to dev dependencies ([`ff0434a`](https://github.com/srv/git/chew/commit/ff0434a03cb14339898a6067b2d7ed24312d16e1))

### Feature

* feat: added new function `fold_many_bounded` ([`1ed1fdf`](https://github.com/srv/git/chew/commit/1ed1fdf2501562f93cc2417f600f7c6dbb7985c3))

* feat: added function fold_many1 ([`836d131`](https://github.com/srv/git/chew/commit/836d131bd0d8ad1dc42b89a7823029fc92762683))

* feat: added fold_many0 function to repeat mod

Added function for supporting custom accumulation operations over a set
of values. ([`b4ee58d`](https://github.com/srv/git/chew/commit/b4ee58d196c4e73a2e58edf03a8da2d48d7dc625))

* feat: added fn fill for filling buffers of content ([`c20d89a`](https://github.com/srv/git/chew/commit/c20d89afd855a4a9355c15ccfd2b4f6860d2e197))

* feat: added generic fn take_while_bounded

Added function `take_while_bounded` which resembles nom&#39;s
`take_while_m_n` for using `take_while` a bounded number of times. ([`75e759c`](https://github.com/srv/git/chew/commit/75e759c9afc30048b2457d75af08ba242a5333bc))

* feat: added new match fn is_alphabetic

Added `is_alphabetic` function, which implements the `Matcher` interface
for string sequences to make matching characters easier. ([`52b800c`](https://github.com/srv/git/chew/commit/52b800cfefa245770dfaf633cb29819abf9ae8de))

* feat: added generic function test_while1 ([`b3c72fd`](https://github.com/srv/git/chew/commit/b3c72fd79dcbcdefd3c609b9445dc14ad77bc4c9))

* feat: added generic function take_until1 ([`c0b3454`](https://github.com/srv/git/chew/commit/c0b3454641f31d4c8ede444b865c60dfa2cb34b7))

* feat: added new generic function take_until ([`396402f`](https://github.com/srv/git/chew/commit/396402f6fa1406871a7090892711123318b93dc1))

* feat: added new fn take_till1 to generic fns ([`7280c80`](https://github.com/srv/git/chew/commit/7280c800353f829c83fe17dc8732282b4e89f148))

* feat: added parser tag_no_case for case-insensitive parsing ([`07d645c`](https://github.com/srv/git/chew/commit/07d645cdac6eb701e2eb7f61f7e953cbbd0de2d5))

### Fix

* fix: fixed type checking issues with new fns ([`446156a`](https://github.com/srv/git/chew/commit/446156a0d22945e5e09508902f086071c81c8823))

### Refactor

* refactor: changed `fill` to accept a wider range of types ([`abddcd3`](https://github.com/srv/git/chew/commit/abddcd3bbffbe97a53afac6d9d748a0bcc91586b))

* refactor: changed type hinting names in types mod ([`d154b8c`](https://github.com/srv/git/chew/commit/d154b8c4a1ca17e5e26026bd59d333f2e152f16c))

* refactor: updated syntax of union aliases in types ([`72f34db`](https://github.com/srv/git/chew/commit/72f34db483212ed936bd6d5daf606c9b65b9dfd8))

* refactor: removed unnecessary error check in alpha0 ([`a274852`](https://github.com/srv/git/chew/commit/a274852cbbef47bc0772442aa790cae6ed4907ae))

* refactor: replaced underlying calls in is_a &amp; is_not

Replaced underlying calls in is_a and is_not to take_while1. ([`f50e664`](https://github.com/srv/git/chew/commit/f50e6648073b05af823af096cfc1b5ff6ffc9403))

* refactor: moved function _min_one into generic mod ([`8fde8c6`](https://github.com/srv/git/chew/commit/8fde8c6ad95c1d83d910d203604036f1c13319cb))

* refactor: removed now-unused import from error module ([`a12887b`](https://github.com/srv/git/chew/commit/a12887b3f5f07cf4be257cf649105bb955a8ff37))

### Test

* test: added coverage.py settings to pyproject.toml ([`d9b4d51`](https://github.com/srv/git/chew/commit/d9b4d51ace4f5337abe3877ddd0f62322d1c7b5b))

* test: refactored tests to use new matcher ([`9e36bef`](https://github.com/srv/git/chew/commit/9e36befab985cddec58212aa184fa21aa7cf1066))


## v3.0.0 (2023-09-22)

### Breaking

* refactor!: removed manual origin holding from Error

Removed the ability for an Error to contain its origin in favor of using
Python&#39;s builtin Exception tracing ability. ([`7c80dde`](https://github.com/srv/git/chew/commit/7c80ddef80e7410ee7f676640c1e50e0739ff703))

### Fix

* fix: fixed bug in satisfy return value

Fixed issue where satisfy would return the post-operated on sequence
instead of the original un-modified sequence. ([`9e0fde4`](https://github.com/srv/git/chew/commit/9e0fde4ba06eafd79017b67333390a707240c7f4))

* fix: fixed satisfy to return the correct type ([`c9733d7`](https://github.com/srv/git/chew/commit/c9733d7afbcbc0a7e7bd610dcd47d4cc48e0bac2))

* fix: fixed return error kind of char function

Fixed the return value of `char` to be `ErrorKind.CHAR` in all cases. ([`e434e61`](https://github.com/srv/git/chew/commit/e434e61e6de4e0b79d7661d7a4a69b2aa0f1fe03))

* fix: fixed tag&#39;s error kind on an exhausted sequence

Fixed the tag function&#39;s return ErrorKind such that it always fails with
an ErrorKind.TAG. ([`84d4a76`](https://github.com/srv/git/chew/commit/84d4a76d0ee5452d95bf5b9597ddeb9710d20e7d))

* fix: fixed return error kind of literal functions

Fixed the return ErrorKind of the literal functions to match the
expected value. ([`cfb3d0a`](https://github.com/srv/git/chew/commit/cfb3d0ac4582615dec405c6f05286310ca1e110a))

* fix: fixed yielded remaining value of tag

Fixed issue where tag would yield the incoming sequence post-comparison
instead of the expected behavior of yielding the rest of the input that
failed to match. ([`ea0f37b`](https://github.com/srv/git/chew/commit/ea0f37b3294f80a5878b9f8590467aaf08baad8c))

### Refactor

* refactor: added a new error kind for the one_of fn ([`41ef3b4`](https://github.com/srv/git/chew/commit/41ef3b4a09b7e971f61ec9dea2d39de54960f6a8))

* refactor: added specific error kind for string.none_of

Added a new ErrorKind for string.none_of. ([`88c89f6`](https://github.com/srv/git/chew/commit/88c89f6020459273bb6dea563ab04b5f51077c95))

* refactor: modified generic.take to use safer interface

Modified `generic.take` to rely on its call to the underlying primitive
`take` when deciding whether or not it can actually take new elements. ([`91237c5`](https://github.com/srv/git/chew/commit/91237c589a399c0f7545d26d7073081ebc170e1c))

### Test

* test: added more comprehensive error tests

Added comprehensive tests for raised exceptions. ([`56ccf05`](https://github.com/srv/git/chew/commit/56ccf056370c2d0875910dbfb62bf2b176ec519b))


## v2.1.0 (2023-09-22)

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
