# All Child exits use Handoff-Back

Every Child exit—including claimed completion, readiness rejection, partial progress, validation failure, capability limits, and execution interruption—is modeled as one Handoff-Back carrying Return State. The Lead alone interprets and accepts that state, avoiding separate success and failure lifecycles while making incomplete coverage observable.
