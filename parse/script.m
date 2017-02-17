(* ::Package:: *)

(*#!/usr/local/bin/MathematicaScript -script*)


filepath=If[Length@$ScriptCommandLine==2
,$ScriptCommandLine[[2]],
FileNameJoin[{NotebookDirectory[], 
"dumps","base_filtered_pu239.json"}]
];
Print[filepath]

data = Import[filepath, "Data"];


name = Last@FileNameSplit[filepath];
basename = First@StringSplit[name, "."]<>"_math.json";
exportFilepath = FileNameJoin@Append[Most@FileNameSplit[filepath],
basename]


getJson[el_]:=Module[
{a1=IsotopeData[el,"AtomicNumber"],
n1=IsotopeData[el,"NeutronNumber"]
},
{"z"-> a1,"a"->(a1+n1)}
]


addChain[element_]:=Module[
{
el=IsotopeData[{"z","a"}/.element,"StandardName"],
chain={},
pos,
result=element,
chainElement,
r1
},
r1=IsotopeData[ToString[el],"BranchingRatios"];
pos=Position[IsotopeData[el,"DecayModes"],"BetaDecay"];
If[Length[pos]==1,
If[Length[r1]>1
&&!MatchQ[r1[[pos[[1,1]]]],_Missing],
AppendTo[result,"ratio"-> r1[[pos[[1,1]]]]]
];
If[Length[r1]==1&&!MatchQ[r1[[1]],_Missing],
AppendTo[result,"ratio"-> r1[[1]]]
];
];
(*Print[result];*)
While[!IsotopeData[el,"Stable"],{
pos=Position[IsotopeData[el,"DecayModes"],"BetaDecay"];
If[Length[pos]==1,{
el=IsotopeData[el,"DaughterNuclides"][[pos[[1,1]]]];
chainElement=getJson[el];
r1=IsotopeData[el,"BranchingRatios"];
If[Length[r1]>1
&&!MatchQ[r1[[pos[[1,1]]]],_Missing],
AppendTo[chainElement,"ratio"-> r1[[pos[[1,1]]]]]
];
If[Length[r1]==1&&!MatchQ[r1[[1]],_Missing],
AppendTo[chainElement,"ratio"-> r1[[1]]]
];
AppendTo[chain,chainElement]
}];
If[Length[pos]==0,Break[]];
}];
AppendTo[result,"chain"-> chain];
result
]


result={};
Dynamic[i]
For[i=1,i<=Length[data],i++,
el=addChain[data[[i]]];
AppendTo[result,el];
]
out = Export[exportFilepath, result];
Print[out]



