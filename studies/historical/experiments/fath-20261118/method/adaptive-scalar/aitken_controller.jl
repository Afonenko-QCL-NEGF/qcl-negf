module ScalarAitkenProposal

export aitken

const α_MIN = 0.10
const α_MAX = 0.80

"""Portable snapshot of the tested weighted scalar proposal.

Pass the previous and current raw defect vectors as collections of equivalent
complex arrays and the fixed norm scale of each array. Supply the preceding
accepted mixing coefficient. The production driver applies the separate
fresh-map admission and fallback policy described in the public report.
"""
function aitken(prev, next, scales, α_previous; initial=.4)
    prev === nothing && return (; α=initial, why="fresh_history", raw=nothing, secant=nothing)
    g, difference, old_norm, new_norm = 0.,0.,0.,0.
    for (old,new,scale) in zip(prev,next,scales)
        go,gd,gn,gm = 0.,0.,0.,0.
        @inbounds for i in eachindex(old,new)
            δ = new[i]-old[i]
            go += real(conj(old[i])*δ)
            gd += abs2(δ)
            gn += abs2(old[i])
            gm += abs2(new[i])
        end
        w = inv(scale^2)
        g += w*go
        difference += w*gd
        old_norm += w*gn
        new_norm += w*gm
    end
    reliable = all(isfinite,(g,difference,old_norm,new_norm)) &&
        difference > 64eps(Float64)*max(old_norm,new_norm,floatmin(Float64))
    reliable || return (; α=.4, why="degenerate_secant", raw=nothing, secant=difference)
    raw = -α_previous*g/difference
    (!isfinite(raw) || raw <= 0) &&
        return (; α=.2, why="nonpositive_secant", raw, secant=difference)
    α = clamp(raw,α_MIN,α_MAX)
    return (; α, why=α==raw ? "secant" : raw<α_MIN ? "clamped_low" : "clamped_high",
            raw, secant=difference)
end

end
