# One Dispatch uses one bidirectional contract

Each Dispatch is governed by one Lead-owned Delegation Contract rather than separate outbound task-packet and inbound return-protocol definitions. Keeping expectation and observation in one contract makes the Lead's acceptance comparison explicit, avoids schema drift between the two directions, and preserves Acceptance Authority at the Lead while allowing every Child exit to return observable work state.
