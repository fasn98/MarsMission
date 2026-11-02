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
    ["Hidrazina", 1004],
];
const CORPOS = [
    { "tipo" : "cilindro", "nome" : "MAV motores do estagio 1 (4 x R-4D-11)", "mat" : -1, "densidade" : 120.916, "cor" : [0.48, 0.37, 0.65], "p0" : [0, 0, 0], "p1" : [0, 0, 0.6], "r" : 0.275 },
    { "tipo" : "tubo", "nome" : "MAV Tanque de oxidante do estagio 1", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "p0" : [0, 0, 0.6], "p1" : [0, 0, 1.24981], "r" : 0.275, "t" : 0.0015 },
    { "tipo" : "cilindro", "nome" : "MAV propelente oxidante do estagio 1", "mat" : 7, "densidade" : 0, "cor" : [0.92, 0.41, 0.2], "p0" : [0, 0, 0.710496], "p1" : [0, 0, 1.13932], "r" : 0.2735 },
    { "tipo" : "tubo", "nome" : "MAV Tanque de combustivel do estagio 1", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "p0" : [0, 0, 1.24981], "p1" : [0, 0, 1.89874], "r" : 0.275, "t" : 0.0015 },
    { "tipo" : "cilindro", "nome" : "MAV propelente combustivel do estagio 1", "mat" : 6, "densidade" : 0, "cor" : [0.16, 0.47, 0.84], "p0" : [0, 0, 1.36029], "p1" : [0, 0, 1.78826], "r" : 0.2735 },
    { "tipo" : "tubo", "nome" : "MAV interestagio", "mat" : 1, "densidade" : 0, "cor" : [0.78, 0.79, 0.81], "p0" : [0, 0, 1.89874], "p1" : [0, 0, 1.99874], "r" : 0.285, "t" : 0.003 },
    { "tipo" : "cilindro", "nome" : "MAV motor do estagio 2 (1 x R-4D-11)", "mat" : -1, "densidade" : 161.221, "cor" : [0.48, 0.37, 0.65], "p0" : [0, 0, 1.99874], "p1" : [0, 0, 2.44874], "r" : 0.1375 },
    { "tipo" : "tubo", "nome" : "MAV Tanque de oxidante do estagio 2", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "p0" : [0, 0, 2.44874], "p1" : [0, 0, 2.82999], "r" : 0.275, "t" : 0.0015 },
    { "tipo" : "cilindro", "nome" : "MAV propelente oxidante do estagio 2", "mat" : 7, "densidade" : 0, "cor" : [0.92, 0.41, 0.2], "p0" : [0, 0, 2.58947], "p1" : [0, 0, 2.68926], "r" : 0.2735 },
    { "tipo" : "tubo", "nome" : "MAV Tanque de combustivel do estagio 2", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "p0" : [0, 0, 2.82999], "p1" : [0, 0, 3.21099], "r" : 0.275, "t" : 0.0015 },
    { "tipo" : "cilindro", "nome" : "MAV propelente combustivel do estagio 2", "mat" : 6, "densidade" : 0, "cor" : [0.16, 0.47, 0.84], "p0" : [0, 0, 2.9707], "p1" : [0, 0, 3.07028], "r" : 0.2735 },
    { "tipo" : "cilindro", "nome" : "MAV carga (conteiner de amostras)", "mat" : -1, "densidade" : 192.414, "cor" : [0.48, 0.37, 0.65], "p0" : [0, 0, 3.21099], "p1" : [0, 0, 3.56099], "r" : 0.275 },
];

annotation { "Feature Type Name" : "MarsMission mav" }
export const marsMissionMav = defineFeature(function(context is Context, id is Id, definition is map)
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
        fCone(context, opId + "n", { "bottomCenter" : vec(b["p0"]), "topCenter" : vec(b["p1"]),
                    "bottomRadius" : b["ri0"] * meter, "topRadius" : b["ri1"] * meter });
        hollow(context, opId + "h", opId + "a", opId + "n");
    }
    else if (t == "caixa")
    {
        fCuboid(context, opId + "a", { "corner1" : vec(b["c1"]), "corner2" : vec(b["c2"]) });
    }
}

// Metodo reaproveitado de projeto anterior: subtracao de corpos (oco) e acabamento (nome, aparencia e material).
function hollow(context is Context, opId is Id, outerId is Id, innerId is Id)
{
    try
    {
        opBoolean(context, opId, {
                    "tools" : qCreatedBy(innerId, EntityType.BODY),
                    "targets" : qCreatedBy(outerId, EntityType.BODY),
                    "operationType" : BooleanOperationType.SUBTRACTION });
    }
    catch (error)
    {
        try
        {
            opDeleteBodies(context, opId + "limpa", { "entities" : qCreatedBy(innerId, EntityType.BODY) });
        }
        catch (error2)
        {
        }
    }
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
