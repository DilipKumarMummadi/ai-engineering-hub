# Scenario

A company runs a .NET modular monolith with PostgreSQL. Leadership wants to "move to microservices". The engineering manager asks for an architecture recommendation.

# Input

Leadership wants us to move to microservices. Please analyze whether we should, and what you'd recommend.

# Context

Requirements and constraints stated by the team:

- The application has six modules: catalog, orders, payments, customers, notifications and reporting. All run in one deployable unit with one PostgreSQL database. Modules call each other in process.
- There are 8 engineers in two teams. No one has run production services on a container orchestrator before. There is a small operations rotation.
- The release process is one pipeline that takes 25 minutes. Releases are weekly and sometimes slip because teams block each other.
- The reporting module runs heavy monthly and ad hoc reports. During report runs, order checkout latency rises noticeably. This is the only module with a scaling or isolation problem the team has observed.
- The team expects to grow to about 15 engineers in 12 months.
- There is no regulatory requirement to isolate any module.
- The budget for new infrastructure is limited but not zero.

# Expected Behavior

The response analyzes the problem rather than following the request's assumption. It identifies the real drivers: release coupling between teams, and reporting load affecting checkout. It separates these from the proposed solution. It presents realistic options, for example keeping the modular monolith with stronger module boundaries, extracting only reporting (or giving it a replica or separate worker), and moving to broad microservices. It weighs each against team size, lack of operations experience, operational overhead, cost and the 12-month growth. It states what each option would improve and what it would cost. It may recommend an incremental path, but it treats the choice as dependent on priorities and says what would favor a different option. It lists open questions and assumptions, for example how reports access data, how teams are organized, and what the checkout latency numbers are, and does not invent them. It covers failure and consistency implications of extracting a service (network failure, data ownership, transactions across modules).

# Important Checks

- The analysis starts from the stated problems and constraints, not from "microservices are good" or "monoliths are good".
- Release coupling and reporting interference are identified as separate problems that may have separate solutions.
- Team size, operational experience and cost are used in the reasoning.
- More than one realistic option is compared, including a low-change option.
- Trade-offs for the extraction of a service include data ownership, consistency and failure handling.
- The migration suggestion, if any, is incremental and reversible.
- Assumptions and open questions are listed. No numbers are invented.
- The response does not claim one architecture is the only correct one.

# Failure Conditions

- Recommending a full microservices split without weighing the constraints.
- Rejecting services outright without analysis.
- Ignoring the operations experience and team size.
- Treating the architecture as broken without evidence.
- Not addressing the reporting interference, which is the one observed technical problem.
- Making up traffic, latency or cost figures.
- Proposing a big-bang rewrite.
- Naming technologies or patterns without tying them to a requirement.

# Notes

Different recommendations are acceptable, for example "extract reporting now and revisit later" or "improve module boundaries first and measure". Evaluate the reasoning and the honesty about trade-offs.
