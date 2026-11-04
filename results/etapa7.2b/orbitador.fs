FeatureScript 3112;
import(path : "onshape/std/geometry.fs", version : "3112.0");

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
    { "tipo" : "esfera_oca", "nome" : "Tanque insercao MON-3 1", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "c" : [1.39739, 0, 0.559891], "r" : 0.561391, "t" : 0.0015 },
    { "tipo" : "esfera", "nome" : "Propelente insercao MON-3 1", "mat" : 7, "densidade" : 0, "cor" : [0.92, 0.41, 0.2], "c" : [1.39739, 0, 0.559891], "r" : 0.550399 },
    { "tipo" : "esfera_oca", "nome" : "Tanque insercao MMH 1", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "c" : [8.55655e-17, 1.39739, 0.559891], "r" : 0.561391, "t" : 0.0015 },
    { "tipo" : "esfera", "nome" : "Propelente insercao MMH 1", "mat" : 6, "densidade" : 0, "cor" : [0.16, 0.47, 0.84], "c" : [8.55655e-17, 1.39739, 0.559891], "r" : 0.550034 },
    { "tipo" : "esfera_oca", "nome" : "Tanque insercao MON-3 2", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "c" : [-1.39739, 1.71131e-16, 0.559891], "r" : 0.561391, "t" : 0.0015 },
    { "tipo" : "esfera", "nome" : "Propelente insercao MON-3 2", "mat" : 7, "densidade" : 0, "cor" : [0.92, 0.41, 0.2], "c" : [-1.39739, 1.71131e-16, 0.559891], "r" : 0.550399 },
    { "tipo" : "esfera_oca", "nome" : "Tanque insercao MMH 2", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "c" : [-2.56697e-16, -1.39739, 0.559891], "r" : 0.561391, "t" : 0.0015 },
    { "tipo" : "esfera", "nome" : "Propelente insercao MMH 2", "mat" : 6, "densidade" : 0, "cor" : [0.16, 0.47, 0.84], "c" : [-2.56697e-16, -1.39739, 0.559891], "r" : 0.550034 },
    { "tipo" : "esfera_oca", "nome" : "Tanque retorno MON-3 1", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "c" : [1.29124, 0, 1.67353], "r" : 0.455243, "t" : 0.0015 },
    { "tipo" : "esfera", "nome" : "Propelente retorno MON-3 1", "mat" : 7, "densidade" : 0, "cor" : [0.92, 0.41, 0.2], "c" : [1.29124, 0, 1.67353], "r" : 0.446051 },
    { "tipo" : "esfera_oca", "nome" : "Tanque retorno MMH 1", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "c" : [7.90659e-17, 1.29124, 1.67353], "r" : 0.455243, "t" : 0.0015 },
    { "tipo" : "esfera", "nome" : "Propelente retorno MMH 1", "mat" : 6, "densidade" : 0, "cor" : [0.16, 0.47, 0.84], "c" : [7.90659e-17, 1.29124, 1.67353], "r" : 0.445756 },
    { "tipo" : "esfera_oca", "nome" : "Tanque retorno MON-3 2", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "c" : [-1.29124, 1.58132e-16, 1.67353], "r" : 0.455243, "t" : 0.0015 },
    { "tipo" : "esfera", "nome" : "Propelente retorno MON-3 2", "mat" : 7, "densidade" : 0, "cor" : [0.92, 0.41, 0.2], "c" : [-1.29124, 1.58132e-16, 1.67353], "r" : 0.446051 },
    { "tipo" : "esfera_oca", "nome" : "Tanque retorno MMH 2", "mat" : 0, "densidade" : 0, "cor" : [0.62, 0.63, 0.66], "c" : [-2.37198e-16, -1.29124, 1.67353], "r" : 0.455243, "t" : 0.0015 },
    { "tipo" : "esfera", "nome" : "Propelente retorno MMH 2", "mat" : 6, "densidade" : 0, "cor" : [0.16, 0.47, 0.84], "c" : [-2.37198e-16, -1.29124, 1.67353], "r" : 0.445756 },
    { "tipo" : "tubo", "nome" : "Cilindro central", "mat" : 1, "densidade" : 0, "cor" : [0.78, 0.79, 0.81], "p0" : [0, 0, 0], "p1" : [0, 0, 2.12727], "r" : 0.7875, "t" : 0.003 },
    { "tipo" : "cilindro", "nome" : "Plataforma (P-016)", "mat" : -1, "densidade" : 213.95, "cor" : [0.48, 0.37, 0.65], "p0" : [0, 0, 2.22727], "p1" : [0, 0, 2.52727], "r" : 1.74499 },
    { "tipo" : "caixa", "nome" : "CCRS", "mat" : -1, "densidade" : 182.353, "cor" : [0.48, 0.37, 0.65], "c1" : [-1.7, -0.25, 2.62727], "c2" : [1.7, 0.25, 4.62727] },
    { "tipo" : "tronco", "nome" : "EES com o conteiner de amostras", "mat" : -1, "densidade" : 429.507, "cor" : [0.48, 0.37, 0.65], "p0" : [0, 0, 4.62727], "p1" : [0, 0, 5.11567], "r0" : 0.6365, "r1" : 0.0064, "ri0" : 0, "ri1" : 0 }
];

const DONO_INTERFACE = 16;

annotation { "Feature Type Name" : "MarsMission orbitador" }
export const marsMissionOrbitador = defineFeature(function(context is Context, id is Id, definition is map)
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
        // Etapa 7.2b: mate connector no plano da interface (z = 0 do modelo), preso ao corpo DONO_INTERFACE.
        opMateConnector(context, id + "interface", {
                    "coordSystem" : coordSystem(vector(0, 0, 0) * meter, vector(1, 0, 0), vector(0, 0, 1)),
                    "owner" : qCreatedBy(id + ("c" ~ toString(DONO_INTERFACE)) + "a", EntityType.BODY) });
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
