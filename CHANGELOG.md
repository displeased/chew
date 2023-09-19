# CHANGELOG



## v2.0.0 (2023-09-19)

### Breaking

* refactor!: refined ErrorKind variants and impl changes ([`fd80921`](https://github.com/srv/git/chew/commit/fd809214378b4ad06c1e685c05e2b974b3fae6f3))

* refactor!: changed is_a and is_not to fail on no match ([`19eafe5`](https://github.com/srv/git/chew/commit/19eafe51eaa1541a1773a3bf554dd5e93cce2fba))

* refactor!: added ErrorKind(s) to Error values ([`2f46bb6`](https://github.com/srv/git/chew/commit/2f46bb642b196221d33472fdbc68b1092fd6550b))

* refactor!: changed names of core types ([`5c651c9`](https://github.com/srv/git/chew/commit/5c651c938532aeed5f1c92e781bd09a0ab077450))

### Feature

* feat: added function for ignoring an ErrorKind to error module ([`8289b8d`](https://github.com/srv/git/chew/commit/8289b8d393aab10c0293c60204b59a48da0f7a48))

* feat: added the ability to chain errors with origins ([`d928698`](https://github.com/srv/git/chew/commit/d92869889629369700dea669f55b8a08606eb958))

### Fix

* fix: fixed Exception type detection ([`e42cbed`](https://github.com/srv/git/chew/commit/e42cbedc0ed0437d4060907c26d711650abbf80b))

* fix: fixed Exception type detection ([`6dabc0c`](https://github.com/srv/git/chew/commit/6dabc0cf4759f6f127cc93c33e286b805e1a1202))

### Refactor

* refactor: changed naming scheme of variable in tag ([`3729858`](https://github.com/srv/git/chew/commit/37298587e1f1e831a8016bd6524c5f76f5bd37e6))

* refactor: changed `map_res` error return semantics ([`603fc83`](https://github.com/srv/git/chew/commit/603fc83f9a048f1bcf5dcf8b14fcbfa1e30fc10a))


## v1.0.0 (2023-09-19)

### Chore

* chore: version 1.0.0 release

* feat: added basic parser combinators

    Added a host of basic parser combinators and a basic framework for
    parsing, including all parsing types.

* fix: fixed multiple in sequence&#39;s return type

    Made multiple return an actual Parser to improve nesting.

* fix: improved result checking for multiple results

    Improved checking for multiple results by clarifying that the Sized
    interface must apply to the returned value.

* refactor: added better typing for string parsing

* build: added Makefile as a command runner

* refactor: modified parsing to be exception-based

* feat: added new combinator for repeating a parser

* refactor: fixed multi code to be more idiomatic

* feat: added more multi parsers

* feat: added new function to parse state for current status

* feat: added more general purpose parser combinators

* refactor: changed to slice-based parsing

* refactor: added generic annotations to sequence fns

* refactor: added better typing to multi module

* refactor: added better generic typing

* refactor: added better typing to primitives

* feat: continued typing improvements

* fix: fixed issue with sequence searching

* build: added makefile target for unit tests

* fix: fixed behavior of generic function to match nom api

* fix: fixed behavior of take_while

* test: added tests for generic functionality

* fix: fixed bug in count implementation

* refactor: renamed character module to char

* fix: fixed type annotations in char functions

* test: added initial tests for chew functionality

* fix: fixed behavior of uint parser

* test: finished adding tests for the multi module

* refactor: made uint and iint into their own parsers

* refactor: converted fns to proper parsers

* refactor: made ParseResult a more lightweight type alias

    We don&#39;t need a dataclass to represent a ParseResult; we can instead
    represent it as a lightweight immutable tuple type.

* refactor: rearranged types and corrects docs

* refactor: rewrote sequence module to use types module

* refactor: rewrote multi to use types module more

* refactor: rewrite generic module to use types module

* refactor: changed comb module to use type module

* refactor: improved typing in branch

* test: updated test semantics to match new parse types

* fix: fixed issues with state updates in multiple parsing

* refactor: change multiple sequence fn to return a tuple

* refactor: fixed naming of preceded

* test: added unit tests for the sequence module

* test: added unit tests for the branch module

* feat: updated combinator functions to reach nom-parity

* fix: fixed eof return value

* fix: fixed negate to actually return a ParseError

* fix: fixed issue with rest raising error

* test: added unit test for combinators

* refactor: removed impossible branch

* refactor: removed unexecuted branch from recognize

* refactor: removed impossible branch from comb module

* refactor: removed unused branches from multi

* refactor: moved sequence primitives into their own module

* refactor: removed non-existent exception catch

* test: added tests for combinator module

* build: added code coverage command runner to Makefile

* build: added targets for cleaning directory to Makefile

* refactor: changed naming convention for parser arguments

* fix: fixed bug introduced by refactoring in tag

* feat: added new primitive function for line number

* build: changed from PDM to Poetry build backend

* build: added development dependencies to pyproject

* build: fixed errors in command runner

* refactor: moved error type into its own module

* test: updated tests with module changes

* refactor: added explicit exports to prevent name conflicts

    Added exports to prevent named generic type conflict on star
    imports.

* test: replaced explicit imports with star imports

* test: rewrote tests to remote unused imports

* test: fixed error introduced in test refactoring

* build: added typing definition marker to package

* feat: added new module `literal` for parsing python-like literals

* refactor: changed multi module to repeat

* refactor: renamed `primitives` module to `primitive`

* refactor: renamed `comb` module to `combine`

* refactor: renamed `char` module to `string`

* refactor: replaced custom string constants with stdlib

* build: added distribution folder to distclean ([`38e25f8`](https://github.com/srv/git/chew/commit/38e25f8fd3126065e633a28d46b6e92fe66be8b8))

* chore: initial commit ([`a65bbd9`](https://github.com/srv/git/chew/commit/a65bbd939393361c532f4d2dca5b73df2ec089a9))
