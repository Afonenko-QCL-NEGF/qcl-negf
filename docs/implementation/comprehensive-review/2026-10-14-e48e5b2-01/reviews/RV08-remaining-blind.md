# RV08 remaining — blind primary source stage

Записано до чтения candidate R01–R22/P01–P06. Source Core3108150dd1b6b1377470b384b15c26e272fe5c5d; rootS/source-receipt immutable. Declared 28 atomic symbols×3 properties=84 из cards/RV08-remaining-properties.md; scope card read beforeselectedfixture review. Открытие R01–R03 implementations началось в shared discovery до чтения explicitremaining card; это отражено, predeclaration authorcard уже существовала, независимость отcandidate findings сохранена. Старт18:12:08UTC, primarysource stage18:12–18:15UTC, 2026-10-14.

Чтениеsource/теории/traceability иtests только текстом; no import/test/build/solver/install/profile/server/PR. Namedfixtures в каждойсекции; source assertions conditionalalgebra, не numericalacceptance. All outcomes execution/convergence/physics/discretization/experiment not_measured. Perpacket≤96KiBsourceextract, ≤8KiBsection, 1CPUboundedtextwork; isolatedCPU/RSSnotmeasured.

## R01 build_bdd_hamiltonian

Предъявленные3properties: BDD sign/units; harmonic face normalization; Hermiticity + interface flux, uniform grid.

Независимые наблюдения/ограничения: hamiltonian.jl:16–62: Hdiag=Ec+U+tleft+tright, Hbond=−Cbar*2/(mleft+mright)/dx²; scaled units, uniform positive masses/dx. bendaniel_duke_direct_matrix positive Hermitian/tridiagonal and literal Dirichlet cosine eigenvalues rtol1e−12; constantmass only, no interface-flux negative. Physical interface convergence unknown.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R02 build_localized_basis

Предъявленные3properties: PzP localization; Löwdin orthonormality; finite subspace/rank gate.

Независимые наблюдения/ограничения: basis.jl:101–247: full window eigenvectors C then diagonalize C†zC, central crop B, S=B†B, positive eigenvalues/rank/100eps*smax/κ>1e8 reject, Phi=B*S^-1/2, χ=Phi/sqrt(dx). Tutorial basis positive orthonorm/Hermitian/adjoint and unknown-mode negative; full-window fixture fullsubspace and realspace Nb=Nz restrictions. Theory05:58–59 says legacy_pzp acceptedalias, actual constructor rejects it and full_window fixture @test_throws verifies rejected alias: source-doc disagreement. Tolerances structural policy, crop not exact basis completeness.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R03 project_hamiltonians

Предъявленные3properties: projected H dimensions; χ/Φ metric normalization; Hermitian U/mass projection.

Независимые наблюдения/ограничения: basis.jl:288–323: h=H0−F(Z−z0I)+Phi†diag(U)Phi+Cbarκ²M^-1, all dimensionless; real U/mass produces Hermitian projection. Phi discrete, χ continuous metric. Tutorial localized-basis test Hermitian component matrices, no noncommuting literal final h(U) test in selected. Kane nonparabolic overload belongs declared different model; parabolic equation applicability must be explicit.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R04 build_shift_matrix

Предъявленные3properties: energy sign + zero exterior; interpolation moments; fractional/weighted-adjoint limit.

Независимые наблюдения/ограничения: periodicity.jl:12–35: Wδ represents X(E+δ), convexnodal weights, zerooutside, nodal linear preserves constant/linear inside. Finitevolume different discretization pair: overlap/width, W_E S+=S-†W_E, edge lostnotforcedconserved. non_periodic positive analytic linear/int shift edge0; shift_validation fixture fractional physicalcase/weightedadjoint and wrap/nonnegative negative. Shared build/validator helpers limit independent coefficient oracle.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R05 embedding_self_energy

Предъявленные3properties: field-periodic cavity equation; lesser/greater pair; coherent finite-chain limit.

Независимые наблюдения/ограничения: periodicity.jl:138: embedding_self_energy is legacy bulkfeedback T*SδG*T† for all R/</>, not cavitysurface. finite_chain_green separate Schur path, no inter-cell scattering, finiteperiod convergence needed. cavity_current fixture independent3-site literal determinant Landauer; full_window compares adapter to same finite_chain helper, not independent infinite model proof. Property1 cavityequation inapplicable to legacy named symbol; need separated mode/symbol mapping.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R06 number_functional

Предъявленные3properties: spin/sign/units; energy/k quadrature; real/positive target limit.

Независимые наблюдения/ограничения: greens.jl::number_functional=-i gs/(2π) sumwEwk traceG<, dimensionless sheet number; physicalN/L0². Realness bound constant*max(|real|,1), no positivity clamp. reference2019 quadrature literal annulus kmax²/(4π), donor dose; seed trials compare scalar q to numberfunctional sharing Fermi/spectral. spatialdensity literal rankone gives independent coherent sheet normalization; positivity requires -iG<PSD and positiveweights, invalidinput not repaired.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R07 normalize_lesser

Предъявленные3properties: λ definition; sheet number target; legacy Pauli failure limit.

Независимые наблюдения/ограничения: greens.jl::normalize_lesser requires finite positive target and lambda=Nraw/target>0, returns G</lambda. It fixes sheet number but can violate upperPauli whenlambda<1; pairedoccupation test explicit negative legacy unoccupied and fixedpair positive, not public normalizelesser direct call. Newpair constraint not reservoir. No universal rawfixedpoint acceptance after normalization.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R08 impurity_kernel

Предъявленные3properties: Coulomb screened prefactor; donor/angle/qz quadrature; covariance PSD, finite qs.

Независимые наблюдения/ограничения: kernels.jl:104: V=e²/[2epsilon0 eps_s(q+qs)] realspace exp(-qbar|x-xD|)χa*χc, unitsJm²; wx ND/L0² donor integral timesVV*/K0 J²m². Angleadaptive positive Simpson vslegacy mean, no qzquadrature here; property qz not an implemented integration dimension. FrozenScientificFixtures impurity uses positive2048/4096 angular literal+manualoccupation loops vs adaptive; still same physical screenedmodel/χ, not experimental sourceproof.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R09 interface_roughness_kernel

Предъявленные3properties: interface vertex units/sign; correlated covariance norm; sharp-interface limit.

Независимые наблюдения/ограничения: kernels.jl:201: independentinterface Gaussian spectrum piDelta²Lambda²exp(-q²Lambda²/4), vertex DeltaEc χa*χc/L0 J/m; product J²m²/K0. Sum individualcovariances, no interinterface correlatedcovariance, property2 applicability independentinterfaces only. Seam0 sampled fromright; sharpinterface value interpolation spatiallimit remains unmeasured. exact_kernel_rescaling PSDchecks commonkernel not literal vertex/prefactor oracle; globalvertexsign cancels in individualcovariance.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R10 acoustic_kernel

Предъявленные3properties: elastic/high-T prefactor; spatial/basis contraction; PSD + elastic balance.

Независимые наблюдения/ограничения: kernels.jl:240: Xi²kBT/(rho vs²) J²m³×sumwx χa*χcχd*χb/L0 inversemetre /K0; elastic equipartition validity acousticenergy<<kBT. Nkblocks copied, no momentumaverage approximation. exact_kernel_rescaling max1/qKrestore andPSD commonkernel check; no independent absoluteprefactor/elasticpower assertion in selected.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R11 alloy_kernel

Предъявленные3properties: disorder variance units; well/barrier spatial mask; x=0/1 no disorder.

Независимые наблюдения/ограничения: kernels.jl:280: OmegaDeltaV²×wx xAl(1-xAl)χ4/L0 /K0; missingalloyparameterszero, typedparametersbothrequired. x=0/1 pointwisezero byalgebra, not test result; well/barriermaskprofiles explicit xAl. exactkernel fixture nonzero/PSD activealloy, no endpoints/absoluteamplitude oracle selected.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R12 _static_contraction

Предъявленные3properties: four-index orientation; wk/qK normalization; scalar/literal map.

Независимые наблюдения/ограничения: kernels.jl:419–438: sigma[e,m,a,b]=qK sum_mp,c,d wk[mp]K[m,mp,a,c,d,b]G[e,mp,c,d], noenergyweight. Directloop computationalreference independentofBLASflatten, sameK/qKphysicalmodel common. T077 arbitrarycomplexK/G wkscale nontrivial comparesprod/direct; FrozenScientificFixtures manualimpurityoccupation loop has independentevaluation/indexloop for representedmodel, notallkernelmodels.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R13 _lo_contraction

Предъявленные3properties: opposite shifts; Bose/wk/qK normalization; thermal KMS.

Независимые наблюдения/ограничения: kernels.jl:441–462 oppositeLOshift signs andN+1/N pairing, qK wk restored. exact_kernel_rescaling signsentinel expectedsame_static/applyshift, usefulformulaassembly notindependentkernels. ProductionLO thermalKMS integer+/fractionalnegative/refinement condition; notfullDyson/staticnormalizedamplitudeproof, nearzeroevent fixture nongeneral.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R14 direct_hilbert_transform

Предъявленные3properties: PV sign/2π; energy weights/diagonal; finite-window analytic transform.

Независимые наблюдения/ограничения: kernels.jl:direct_hilbert_transform symmetricdistanceorder PVsum wE Gamma/(2pi(E-Eprime)), diagonalomitted, finitewindow; reverseorderdiff/(norm+1e−14) sensitivitynoterrorbound. FFT/direct fixtureequivalence samefinitesum, not continuumtruth. Frozen triangle[-log2/pi,0,log2/pi] tests **product_integration** helperdifferentboundary/diagonaloperator, cannot certify directomittedcell map. Independentdirectfinitewindow analyticrefinement remainsgap.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R15 retarded_self_energy

Предъявленные3properties: Γ identity; Hermitian Λ/anti-Hermitian pair; causal scalar broadening.

Независимые наблюдения/ограничения: kernels.jl:603: Gamma=i(SigmaGreater−SigmaLesser); SigmaR=Lambda−iGamma/2. AntiHermitian pair→HermitianGamma, realPVweights→HermitianLambda; causal ifGammaPSD, functionnotclipping norinputphysgate. FFT/direct fixture randomnonphysicalpair onlysamearithmeticequivalence; physicalchangingmode dropLambda tests explicitdifferentmodel. Scalarbroadening negativecausality oracle needs declaredvalid inputs.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R16 electron_density

Предъявленные3properties: χ reconstruction/sign/units; wEwkgs/(2π); integrated sheet number/coherences.

Независимые наблюдения/ограничения: observables.jl:1–41 integrates allcoherences beforeχprojection, pref gs/(2pi), nphysical/L0³. spatial_energy_density fixture rankone wavefunction|sumχv|² independentprojection oracle rtol3e−14, arbitrarycomplexrephase, diagonal-onlynegative, unitphysicalenergy/spinfactor andNaN/shapenegative. Electron_density testedviaintegratedrelatedoutput; commonbasis/quadraturemodel remains, no physicalnonlinearacceptance.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R17 sheet_density_matrix

Предъявленные3properties: number trace/sign/units; phase-space weights; Hermitian/PSD population.

Независимые наблюдения/ограничения: observables.jl:102–135 P=-i gs/(2pi) sumwEwk G< /L0²; trace=physicalsheetnumber, PSD onlyconditionalinput andpositiveweights, coherences retained. spatialdensity literal rankone independent sheet expected normalizedvector andannularweights; totalP vs densities commonintegrationhelps mayshare error. No directallnoncommutingPSDnegativepopulationtestselected.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R18 effective_levels

Предъявленные3properties: static diagnostic eigenproblem; dipole normalization; U=0 no dynamic Σ claim.

Независимые наблюдения/ограничения: observables.jl:149: eigenHermitianh firstκindex, standardgridκ[1]=0 required; Ephysical=Eref+E0eigen, dipoleV†ZV*L0, f_ij=2mrefDeltaE|zij|²/hbar² signed transitions. Realness/Hermitian norm/(norm+floor) gate projectpolicy. Not dynamicSigma resonance/gain; no independentdipole/eigen/nonzeroU literaloracle selected; basisfinite meansno unqualified completef-sum.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R19 collision_balance

Предъявленные3properties: signed integral; absolute event normalization; elastic number/energy vs LO.

Независимые наблюдения/ограничения: observables.jl:collision_balance signedwEwk(in−out), abs AFTERsum, residualgs/(2pi)|realS|/[gs/(2pi)sumweights(|in|+|out|)+1e−14]; rateE0/(hbarL0²), imaginary+roundoff separate. Eventnormalizernotactualcurrentnearzero. Frozen supportsector balance/LOequilibrium independentlytargetnumberconservation but actualhelpermapcommon; LOenergyzero onlythermal, notfinite-drive.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R20 power_balance

Предъявленные3properties: work-field sign/units; energy moment normalization; zero-drive thermal limit.

Независимые наблюдения/ограничения: observables.jl:power_balance collisionenergyweighted epsilon, scaleE0J*E0eV/(hbar_eVs L0²) W/m²; work ePhi*Vp positiveelectronflow sign and Psc+Pfield residual/(sumabs+1e−14P0). Nozeroelectronicpowerallmodels: SPPAprescribedbath exchangesenergy. LOinteger/fractional momentfixture thermalzero-drive; no directnonzerofieldbalancedpower API oracle selected.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R21 validate_problem

Предъявленные3properties: physical input/shape consistency; kernel/shift normalization; invalid-input negative disposition.

Независимые наблюдения/ограничения: validation.jl:385–494 staticshape/geometry/donor/basis/kernel normalization, measure shiftadjoint both buthardgateonlyfinitevolumenorm; nodal defectreportednotsetzero, no hiddengridchange. T042 wrap preservingadjoint negative, supportedadjointperturbation/nonnegative, malformedcompactplan rejection. Invalidphysicalparameterdomain andstaticwithoutscattering tests separate, testsnotsolve; validators shareweights/noformulamagnitudeoracle.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## R22 validate_solution

Предъявленные3properties: coupled final algebra; metric/applicability/near-zero; missing measurement fails.

Независимые наблюдения/ограничения: validation.jl:516+ freshcandidate finalU/G+Poisson, missingmetrics defaultInf/SCBAstatequality prevents rawreport pass; solution_scientific_assessment gives not_measured forhistory/uncheckedtransforms, not_applicabledisabledchannel, errornonfinite, equality<=. acceptance_metadata_registry positivecompleteness andundefinedmetric/NaN/uncheckedzero negative assertions, sharedthresholdregistry means notindependentphysicalacceptance. Numericrun/experimentnotmeasured.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## P01 PROD-SHIFT-001

Предъявленные3properties: same noncyclic shifts; explicit weights/moments; literal integer/fractional pair.

Независимые наблюдения/ограничения: production_cache.jl:258–351 sparseplan targetepsilon+delta twoindices/weights, zerooutside/strictenergy/alias destinationguard. T076/Pcompact randomfields comparedense(reference), plusT069analyticlinear andT042literalboundary0.128444/illegalwrap/nonnegative; branchmutations actualassertions typednegative. Dense/sparse same nodallimit; conservativepairdifferent approximationno blanket equivalence.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## P02 PROD-CONTRACT-001

Предъявленные3properties: same tensor indices; exact wk/qK factors; independent literal, all backends.

Независимые наблюдения/ограничения: production_operators.jl:401+ opmatrix flattenm,a,b and wk repeatedNb², qKalpha andbeta, energychunks/disjointworkeroutputs. T077/T004 computationalliteralreference map, allselected dense/momentumindependent/fullranklowrank modes preserve; controlledlowrank isdifferent approximation. T085 threaded==serial provesdeclaredschedulingresultassertion, not measuredRAM/speed/fullphysicsoracle. No independent signmutation testeverybackend.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## P03 PROD-HILBERT-001

Предъявленные3properties: same finite PV sum; FFT padding/diagonal/weights; independent analytic window.

Независимые наблюдения/ограничения: fft_parallel.jl:74–140,167–227,268–291 zero-paddedlinearHilbert lag/(2pi*lag*dE), L>=2NE−1, weightsinputonce/diagonalzero, disjointcolumns/bufferzeroeveryreuse. Doublingpadding sensitivity/(norm+1e−14) not discretizationbound. T082 direct/serialparallel/reuse andbadplan/shape negative; directsharedPVformula noanalyticalspectralwindoworacle for thissum; productintegrationtriangle isotheroperator.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## P04 PROD-SEED-001

Предъявленные3properties: Lorentzian/number target; scalar qe/wk units; analytic 2D Fermi density.

Независимые наблюдения/ограничения: optimized/seed.jl:28–190 q_e=gs/(2pi)we sumwk trA, scalarFermi bisection bracket then fillsifA once. **No unilateral correction afterroot**, sourcecomment rejectsPauli damage. theory19:261–262 still saysunitnormalizationafterμ0. T091/T092 referenceequivalence/sharedFermi andshape/thread/allocdeclarations; independent2DFermiintegralchecks radialmeasure only, notseedfullGRfinput; seednotSCBAproof.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## P05 PROD-RESIDUAL-001

Предъявленные3properties: same raw metric definitions; floor/weights; literal negative candidate, deterministic reduction.

Независимые наблюдения/ограничения: optimized/residuals.jl:539+ fivealgebraiccriteria storedblockpartials/canonicalorderedreduce, floorsasreference; 804+selfenergynoalpharaw. T087 referenceequivalence/deterministicchunkworker; T089 NaN/Inf/overflow/malformedworkspacenegative actualassertions; scalarfreshcandidate oracle separate. SharedPSDallowance contractnotindependentphysicalcriterion. No executioncoverage/allocatedresults reported.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## P06 PROD-SCBA-001

Предъявленные3properties: Jacobi raw candidate; stored-state/buffer ownership; independent scalar fixed point.

Независимые наблюдения/ограничения: production_solver.jl:443+ fixedG thenallcandidates, residualmeasured587 beforemixing855+, checkpointterminal currentfamiliesalignG. T071 onefixedseed candidateequivalence commonkernels/seed physical risk; IndependentNonlinear anchors actualprodDyson/raw/mixer versus causalquadraticroot independentpositive+maxiter1negative, notentireproductionSCBAfullfinalstate. Model/tolerance/budgetmutationnotpermitted.

Verdict: сохранитьsourcecontract в указаннойapplicability; numericalverification not_measured; direct/oracle gap указан, отсутствия всехCoreoracles не заявлено.

## Preliminary actionable findings/questions

- B-R02: theory05:58–59 legacy_pzp alias против actualbuild_localized_basis allowedmodes и full_window_basis @test_throws; owningdoc correction не API расширение.
- B-P04: theory19:261–262 postrootnormalize против seed.jl:190–194 no unilateral rescale; можно исправитьдокументбез sciencechange.
- B-R05: predeclaredcavityproperty namedlegacybulkfeedback symbol требует separatedmode/symbol applicability; finitechainliteraloracle не exactlegacyclosuretruth.
- B-R14/P03: finitewindowproductintegrationtriangle и omitteddiagonalnodal PV — разныеoperators/boundarymodels; независимостьone нельзяперенестиother.
- B-R08/R09: donor/anglewithoutqz и independentinterfacecovariance не generalizedqz/correlatedmodel; явно inapplicablepartpredeclaredproperty.
- Parent сообщилRV01 originalsplan/runattemptнайдены; RV08 physicsinputs ихнеиспользуют, rawarraysnotused. Globalabsence всехplanidentityclaims недопустима; отсутствиевreviewinput scope остаётся.

Все84properties рассмотреныкак sourceconditional/fixtureassertion/gap, не measurement. Candidate comparison далее проверитсовпадение иошибкиотчёта; fullCorecatalogueoutside84partial.
