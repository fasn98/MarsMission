FeatureScript 2737;
import(path : "onshape/std/geometry.fs", version : "2737.0");

// MarsMission - CAD parametrico (Fase 7, Etapa 7.2). ARQUIVO GERADO por tools/cad_parametros.py a partir de
// cad/featurescript/modelo.fs e de results/: nao editar a mao. Este modelo nao tem nenhuma dimensao; ele so constroi os
// corpos da lista CORPOS (metros, kg/m^3), gerada pela ferramenta a partir de results/ e config/.
// Eixos: z = eixo do veiculo (lancamento: altura acima do plano do PAF). Cada corpo recebe nome, aparencia e material,
// para as Mass Properties do Onshape. Corpos com "mat" = -1 usam a densidade equivalente do proprio corpo (massa do
// orcamento / volume, premissa P-094).
// O cabecalho (versao do FeatureScript e da biblioteca padrao) deve ser trocado pelo do Feature Studio criado na conta.

const MATERIAIS = [
    ["Ti-6Al-4V", 4424],
    ["Al 2219", 2840],
    ["Al 7075", 2800],
    ["CFRP IM7/8552 (fita unidirecional)", 1574],
    ["PICA", 274],
    ["SLA-561V", 256],
    ["MMH", 869],
    ["MON-3", 1431],
    ["Hidrazina", 1004]
];
const CORPOS = [
    { "tipo" : "tronco", "nome" : "Nariz do escudo (PICA)", "mat" : 4, "densidade" : 0, "cor" : [0.35, 0.22, 0.12], "p0" : [0, 0, 3.97], "p1" : [0, 0, 3.95], "r0" : 0.005, "r1" : 0.25, "ri0" : 0, "ri1" : 0 },
    { "tipo" : "tronco_oco", "nome" : "Escudo termico (PICA)", "mat" : 4, "densidade" : 0, "cor" : [0.35, 0.22, 0.12], "p0" : [0, 0, 3.95], "p1" : [0, 0, 3.12], "r0" : 0.25, "r1" : 2.34, "ri0" : 0.160913, "ri1" : 2.25091, "pe0" : [0, 0, 3.98195167027], "pe1" : [0, 0, 3.03091], "rie0" : 0.0804565, "rie1" : 2.47524473823 },
    { "tipo" : "tronco_oco", "nome" : "Casca traseira 1 (SLA-561V)", "mat" : 5, "densidade" : 0, "cor" : [0.85, 0.8, 0.62], "p0" : [0, 0, 3.12], "p1" : [0, 0, 1.97], "r0" : 2.34, "r1" : 1.75, "ri0" : 2.32568, "ri1" : 1.73568, "pe0" : [0, 0, 3.13432], "pe1" : [0, 0, 1.95568], "rie0" : 2.33302678261, "rie1" : 1.72833321739 },
    { "tipo" : "tronco_oco", "nome" : "Casca traseira 2 (SLA-561V)", "mat" : 5, "densidade" : 0, "cor" : [0.85, 0.8, 0.62], "p0" : [0, 0, 1.97], "p1" : [0, 0, 1.37], "r0" : 1.75, "r1" : 1.2, "ri0" : 1.73267, "ri1" : 1.18267, "pe0" : [0, 0, 1.98733], "pe1" : [0, 0, 1.35267], "rie0" : 1.74855583333, "rie1" : 1.16678416667 },
    { "tipo" : "tronco_oco", "nome" : "Casca traseira 3 (SLA-561V)", "mat" : 5, "densidade" : 0, "cor" : [0.85, 0.8, 0.62], "p0" : [0, 0, 1.37], "p1" : [0, 0, 0.12], "r0" : 1.2, "r1" : 0.4, "ri0" : 1.18478, "ri1" : 0.384777, "pe0" : [0, 0, 1.385223], "pe1" : [0, 0, 0.104777], "rie0" : 1.19452275654, "rie1" : 0.375034243465 },
    { "tipo" : "cilindro", "nome" : "Tampa traseira (SLA-561V)", "mat" : 5, "densidade" : 0, "cor" : [0.85, 0.8, 0.62], "p0" : [0, 0, 0.12], "p1" : [0, 0, 0.1327], "r" : 0.4 },
    { "tipo" : "esfera_oca", "nome" : "Tanque cruzeiro MON-3", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "c" : [1.5, 0, 0.351727], "r" : 0.233227, "t" : 0.0015 },
    { "tipo" : "esfera", "nome" : "Propelente cruzeiro MON-3", "mat" : 7, "densidade" : 0, "cor" : [0.92, 0.41, 0.2], "c" : [1.5, 0, 0.351727], "r" : 0.227799 },
    { "tipo" : "esfera_oca", "nome" : "Tanque cruzeiro MMH", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "c" : [-1.5, 0, 0.351727], "r" : 0.233227, "t" : 0.0015 },
    { "tipo" : "esfera", "nome" : "Propelente cruzeiro MMH", "mat" : 6, "densidade" : 0, "cor" : [0.16, 0.47, 0.84], "c" : [-1.5, 0, 0.351727], "r" : 0.227648 },
    { "tipo" : "cilindro", "nome" : "Circuito de fluido de cruzeiro (P-077)", "mat" : -1, "densidade" : 21.6793, "cor" : [0.48, 0.37, 0.65], "p0" : [0, 0, 0], "p1" : [0, 0, 0.12], "r" : 2.09 },
    { "tipo" : "esfera_oca", "nome" : "Tanque descida 1", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "c" : [1.4, 0, 3.12], "r" : 0.358245, "t" : 0.0015 },
    { "tipo" : "esfera", "nome" : "Propelente descida 1", "mat" : 8, "densidade" : 0, "cor" : [0.11, 0.69, 0.48], "c" : [1.4, 0, 3.12], "r" : 0.350697 },
    { "tipo" : "esfera_oca", "nome" : "Tanque descida 2", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "c" : [-0.7, 1.21244, 3.12], "r" : 0.358245, "t" : 0.0015 },
    { "tipo" : "esfera", "nome" : "Propelente descida 2", "mat" : 8, "densidade" : 0, "cor" : [0.11, 0.69, 0.48], "c" : [-0.7, 1.21244, 3.12], "r" : 0.350697 },
    { "tipo" : "esfera_oca", "nome" : "Tanque descida 3", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "c" : [-0.7, -1.21244, 3.12], "r" : 0.358245, "t" : 0.0015 },
    { "tipo" : "esfera", "nome" : "Propelente descida 3", "mat" : 8, "densidade" : 0, "cor" : [0.11, 0.69, 0.48], "c" : [-0.7, -1.21244, 3.12], "r" : 0.350697 },
    { "tipo" : "cilindro", "nome" : "Nucleo do lander (P-017 sem braco e helicopteros)", "mat" : -1, "densidade" : 1041.79, "cor" : [0.48, 0.37, 0.65], "p0" : [0, 0, 3.42], "p1" : [0, 0, 3.12], "r" : 1.33458 },
    { "tipo" : "cilindro", "nome" : "MAV motores do estagio 1 (4 x R-4D-11)", "mat" : -1, "densidade" : 120.916, "cor" : [0.48, 0.37, 0.65], "p0" : [0, -1.7805, 2.835], "p1" : [0, -1.1805, 2.835], "r" : 0.275 },
    { "tipo" : "tubo", "nome" : "MAV Tanque de oxidante do estagio 1", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "p0" : [0, -1.1805, 2.835], "p1" : [0, -0.530685, 2.835], "r" : 0.275, "t" : 0.0015 },
    { "tipo" : "cilindro", "nome" : "MAV propelente oxidante do estagio 1", "mat" : 7, "densidade" : 0, "cor" : [0.92, 0.41, 0.2], "p0" : [0, -1.07, 2.835], "p1" : [0, -0.641181, 2.835], "r" : 0.2735 },
    { "tipo" : "tubo", "nome" : "MAV Tanque de combustivel do estagio 1", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "p0" : [0, -0.530685, 2.835], "p1" : [0, 0.11824, 2.835], "r" : 0.275, "t" : 0.0015 },
    { "tipo" : "cilindro", "nome" : "MAV propelente combustivel do estagio 1", "mat" : 6, "densidade" : 0, "cor" : [0.16, 0.47, 0.84], "p0" : [0, -0.420207, 2.835], "p1" : [0, 0.0077614, 2.835], "r" : 0.2735 },
    { "tipo" : "tubo", "nome" : "MAV interestagio", "mat" : 1, "densidade" : 0, "cor" : [0.78, 0.79, 0.81], "p0" : [0, 0.11824, 2.835], "p1" : [0, 0.21824, 2.835], "r" : 0.285, "t" : 0.003 },
    { "tipo" : "cilindro", "nome" : "MAV motor do estagio 2 (1 x R-4D-11)", "mat" : -1, "densidade" : 161.221, "cor" : [0.48, 0.37, 0.65], "p0" : [0, 0.21824, 2.835], "p1" : [0, 0.66824, 2.835], "r" : 0.1375 },
    { "tipo" : "tubo", "nome" : "MAV Tanque de oxidante do estagio 2", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "p0" : [0, 0.66824, 2.835], "p1" : [0, 1.04949, 2.835], "r" : 0.275, "t" : 0.0015 },
    { "tipo" : "cilindro", "nome" : "MAV propelente oxidante do estagio 2", "mat" : 7, "densidade" : 0, "cor" : [0.92, 0.41, 0.2], "p0" : [0, 0.80897, 2.835], "p1" : [0, 0.908758, 2.835], "r" : 0.2735 },
    { "tipo" : "tubo", "nome" : "MAV Tanque de combustivel do estagio 2", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "p0" : [0, 1.04949, 2.835], "p1" : [0, 1.4305, 2.835], "r" : 0.275, "t" : 0.0015 },
    { "tipo" : "cilindro", "nome" : "MAV propelente combustivel do estagio 2", "mat" : 6, "densidade" : 0, "cor" : [0.16, 0.47, 0.84], "p0" : [0, 1.1902, 2.835], "p1" : [0, 1.28979, 2.835], "r" : 0.2735 },
    { "tipo" : "cilindro", "nome" : "MAV carga (conteiner de amostras)", "mat" : -1, "densidade" : 192.414, "cor" : [0.48, 0.37, 0.65], "p0" : [0, 1.4305, 2.835], "p1" : [0, 1.7805, 2.835], "r" : 0.275 },
    { "tipo" : "cilindro", "nome" : "Braco de coleta (guardado)", "mat" : -1, "densidade" : 4794.97, "cor" : [0.48, 0.37, 0.65], "p0" : [0.45, -1.175, 3.07], "p1" : [0.45, 1.175, 3.07], "r" : 0.05 },
    { "tipo" : "cilindro", "nome" : "Helicoptero 1", "mat" : -1, "densidade" : 4.22579, "cor" : [0.48, 0.37, 0.65], "p0" : [0, -0.75, 2.5], "p1" : [0, -0.75, 2.01], "r" : 0.7 },
    { "tipo" : "cilindro", "nome" : "Helicoptero 2", "mat" : -1, "densidade" : 4.22579, "cor" : [0.48, 0.37, 0.65], "p0" : [0, 0.75, 2.5], "p1" : [0, 0.75, 2.01], "r" : 0.7 }
];

annotation { "Feature Type Name" : "MarsMission lander" }
export const marsMissionLander = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Assign materials" }
        definition.assignMaterials is boolean;
    }
    {
        for (var i = 0; i < size(CORPOS); i += 1)
        {
            const b = CORPOS[i];
            const cid = id + ("c" ~ toString(i));
            constroi(context, cid, b);
            var mat = ["", 0];
            if (b["mat"] < 0)
            {
                mat = [b["nome"] ~ " (densidade equivalente)", b["densidade"]];
            }
            else
            {
                mat = MATERIAIS[b["mat"]];
            }
            finish(context, qCreatedBy(cid + "a", EntityType.BODY), b["nome"], mat,
                color(b["cor"][0], b["cor"][1], b["cor"][2]), definition.assignMaterials);
        }
    });

function vec(p is array) returns Vector
{
    return vector(p[0], p[1], p[2]) * meter;
}

/** Constroi um corpo primitivo; o corpo final fica sob o id opId + "a". */
function constroi(context is Context, opId is Id, b is map)
{
    const t = b["tipo"];
    if (t == "cilindro")
    {
        fCylinder(context, opId + "a", { "bottomCenter" : vec(b["p0"]), "topCenter" : vec(b["p1"]), "radius" : b["r"] * meter });
    }
    else if (t == "tubo")
    {
        fCylinder(context, opId + "a", { "bottomCenter" : vec(b["p0"]), "topCenter" : vec(b["p1"]), "radius" : b["r"] * meter });
        const d = normalize(vector(b["p1"][0] - b["p0"][0], b["p1"][1] - b["p0"][1], b["p1"][2] - b["p0"][2])) * b["t"] * meter;
        fCylinder(context, opId + "n", { "bottomCenter" : vec(b["p0"]) - d, "topCenter" : vec(b["p1"]) + d, "radius" : (b["r"] - b["t"]) * meter });
        hollow(context, opId + "h", opId + "a", opId + "n");
    }
    else if (t == "esfera")
    {
        opSphere(context, opId + "a", { "center" : vec(b["c"]), "radius" : b["r"] * meter });
    }
    else if (t == "esfera_oca")
    {
        opSphere(context, opId + "a", { "center" : vec(b["c"]), "radius" : b["r"] * meter });
        opSphere(context, opId + "n", { "center" : vec(b["c"]), "radius" : (b["r"] - b["t"]) * meter });
        hollow(context, opId + "h", opId + "a", opId + "n");
    }
    else if (t == "tronco")
    {
        fCone(context, opId + "a", { "bottomCenter" : vec(b["p0"]), "topCenter" : vec(b["p1"]),
                    "bottomRadius" : b["r0"] * meter, "topRadius" : b["r1"] * meter });
    }
    else if (t == "tronco_oco")
    {
        fCone(context, opId + "a", { "bottomCenter" : vec(b["p0"]), "topCenter" : vec(b["p1"]),
                    "bottomRadius" : b["r0"] * meter, "topRadius" : b["r1"] * meter });
        // cone interno estendido alem das faces (pe0, pe1, rie0, rie1, calculados pela ferramenta): sem faces coplanares
        fCone(context, opId + "n", { "bottomCenter" : vec(b["pe0"]), "topCenter" : vec(b["pe1"]),
                    "bottomRadius" : b["rie0"] * meter, "topRadius" : b["rie1"] * meter });
        hollow(context, opId + "h", opId + "a", opId + "n");
    }
    else if (t == "caixa")
    {
        fCuboid(context, opId + "a", { "corner1" : vec(b["c1"]), "corner2" : vec(b["c2"]) });
    }
}

// Metodo reaproveitado de projeto anterior: subtracao de corpos (oco) e acabamento (nome, aparencia e material).
// Sem recuperacao silenciosa: se a subtracao falhar, a feature falha, em vez de deixar um corpo macico com massa errada.
function hollow(context is Context, opId is Id, outerId is Id, innerId is Id)
{
    opBoolean(context, opId, {
                "tools" : qCreatedBy(innerId, EntityType.BODY),
                "targets" : qCreatedBy(outerId, EntityType.BODY),
                "operationType" : BooleanOperationType.SUBTRACTION });
}

function finish(context is Context, bodies is Query, name is string, mat is array, c is Color, assign is boolean)
{
    try
    {
        setProperty(context, { "entities" : bodies, "propertyType" : PropertyType.NAME, "value" : name });
    }
    catch (error)
    {
    }
    try
    {
        setProperty(context, { "entities" : bodies, "propertyType" : PropertyType.APPEARANCE, "value" : c });
    }
    catch (error)
    {
    }
    if (assign)
    {
        try
        {
            setProperty(context, { "entities" : bodies, "propertyType" : PropertyType.MATERIAL,
                        "value" : material(mat[0], mat[1] * kilogram / meter ^ 3) });
        }
        catch (error)
        {
        }
    }
}
