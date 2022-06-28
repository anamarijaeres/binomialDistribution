This code takes as an input two parameters n and p.
n should have as an initial value the parameter failure locktime which is specific for each protocol
-failure locktime for HTLC-based payment protocol should be determined with respect to number of hops
to receiver using this formula:
    failure_locktime = hops_to_receiver + k * hops_to_receiver
  -k is the factor which in a way sets the delay of HTLC
-failure locktime for Blitz protocol should be determined with respect to number of hops
to receiver using this formula:
    failure_locktime = 2 * hops_to_receiver
The first numerator denotes the locking phase and the second the revoking phase of the protocol.
Depending on which protocol we want to test and the number of hops to the receiver the failure timelock will differ.
Example:
hops to the receiver=3

running code for Blitz:
failure_locktime = 6 --> n = 6
p can be arbitrary

running code for HTLC:
if k = 5:
    failure_locktime = 18 --> n = 18
p can be arbitrary

