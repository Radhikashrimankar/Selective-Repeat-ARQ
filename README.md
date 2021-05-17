# Selective-Repeat-ARQ
Selective repeat ARQ is a data link layer protocol that uses sliding window method for reliable delivery of data frames.

#########################################################
In SR protocol, sender window size is always same as receiver window size.
Here in py file SR protocol does not accept the corrupted frames but does not silently discard them.
SR protocol requires sorting at the receiver’s side.
SR protocol leads to retransmission of lost frames after expiry of time out timer.
#############################################################
