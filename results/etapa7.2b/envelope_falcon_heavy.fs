FeatureScript 3112;
import(path : "onshape/std/geometry.fs", version : "3112.0");

// MarsMission - VERIFICACAO geometrica do modelo (Etapa 7.2b), nao validacao. ARQUIVO GERADO por tools/encaixe_coifas.py a
// partir de cad/featurescript/envelope.fs e de results/: nao editar a mao. Este modelo nao tem nenhuma dimensao.
// Envelope: perfil amostrado do STEP de keep-in do fabricante [F82] p. 16, Tab. 4-1. Plano: origem do arquivo, premissa P-096.
// O envelope e uma casca fina e sem material: a face INTERNA e o limite do volume utilizavel, e a espessura nao tem sentido
// fisico. Com uma casca, Check interference so acusa o que atravessa o limite; um solido acusaria o veiculo inteiro.
// Eixos: z = altura acima da base do veiculo; o plano da interface fica abaixo dela pela altura do adaptador (P-097). Segmentos em metros: [z0, z1, r0, r1].

export enum LeituraEnvelope
{
    annotation { "Name" : "Keep-in do fabricante, faixas de 500 mm" }
    L0
}
const OPCOES = [LeituraEnvelope.L0];
const SEGMENTOS = [
    { "interno" : [[-0.137, -0.127, 2.323, 2.323], [-0.127, 0.373, 2.323, 2.3201], [0.373, 0.873, 2.3201, 2.316], [0.873, 1.373, 2.316, 2.3118], [1.373, 1.873, 2.3118, 2.3077], [1.873, 2.373, 2.3077, 2.3035], [2.373, 2.873, 2.3035, 2.2994], [2.873, 3.373, 2.2994, 2.2953], [3.373, 3.873, 2.2953, 2.2911], [3.873, 4.373, 2.2911, 2.287], [4.373, 4.873, 2.287, 2.2827], [4.873, 5.373, 2.2827, 2.2787], [5.373, 5.873, 2.2787, 2.2745], [5.873, 6.373, 2.2745, 2.2704], [6.373, 6.873, 2.2704, 2.2606], [6.873, 7.373, 2.2606, 2.2099], [7.373, 7.873, 2.2099, 2.1051], [7.873, 8.373, 2.1051, 1.9619], [8.373, 8.873, 1.9619, 1.7996], [8.873, 9.373, 1.7996, 1.5966], [9.373, 9.873, 1.5966, 1.3356], [9.873, 10.373, 1.3356, 1.0023], [10.373, 10.873, 1.0023, 0.5787], [10.873, 11.2206, 0.5787, 0.005]], "externo" : [[-0.127, 0.373, 2.333, 2.3301], [0.373, 0.873, 2.3301, 2.326], [0.873, 1.373, 2.326, 2.3218], [1.373, 1.873, 2.3218, 2.3177], [1.873, 2.373, 2.3177, 2.3135], [2.373, 2.873, 2.3135, 2.3094], [2.873, 3.373, 2.3094, 2.3053], [3.373, 3.873, 2.3053, 2.3011], [3.873, 4.373, 2.3011, 2.297], [4.373, 4.873, 2.297, 2.2927], [4.873, 5.373, 2.2927, 2.2887], [5.373, 5.873, 2.2887, 2.2845], [5.873, 6.373, 2.2845, 2.2804], [6.373, 6.873, 2.2804, 2.2706], [6.873, 7.373, 2.2706, 2.2199], [7.373, 7.873, 2.2199, 2.1151], [7.873, 8.373, 2.1151, 1.9719], [8.373, 8.873, 1.9719, 1.8096], [8.873, 9.373, 1.8096, 1.6066], [9.373, 9.873, 1.6066, 1.3456], [9.873, 10.373, 1.3456, 1.0123], [10.373, 10.873, 1.0123, 0.5887], [10.873, 11.2206, 0.5887, 0.015], [11.2206, 11.2306, 0.015, 0.015]] }
];
const NOME = "Envelope Falcon Heavy (referencia, sem material)";
const COR = [0.15, 0.55, 0.85, 0.25];
const Z_INTERFACE = 0;

annotation { "Feature Type Name" : "MarsMission envelope Falcon Heavy" }
export const marsMissionEnvelopeFalconHeavy = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Leitura do envelope" }
        definition.leitura is LeituraEnvelope;
    }
    {
        var dados = SEGMENTOS[0];
        for (var i = 0; i < size(OPCOES); i += 1)
        {
            if (OPCOES[i] == definition.leitura)
            {
                dados = SEGMENTOS[i];
            }
        }
        pilha(context, id + "ext", dados["externo"]);
        pilha(context, id + "int", dados["interno"]);
        // Sem recuperacao silenciosa: se a subtracao falhar, a feature falha.
        opBoolean(context, id + "casca", {
                    "tools" : qCreatedBy(id + "int", EntityType.BODY),
                    "targets" : qCreatedBy(id + "ext", EntityType.BODY),
                    "operationType" : BooleanOperationType.SUBTRACTION });
        const corpo = qCreatedBy(id + "ext", EntityType.BODY);
        setProperty(context, { "entities" : corpo, "propertyType" : PropertyType.NAME, "value" : NOME });
        setProperty(context, { "entities" : corpo, "propertyType" : PropertyType.APPEARANCE,
                    "value" : color(COR[0], COR[1], COR[2], COR[3]) });
        opMateConnector(context, id + "interface", {
                    "coordSystem" : coordSystem(vector(0, 0, Z_INTERFACE) * meter, vector(1, 0, 0), vector(0, 0, 1)),
                    "owner" : corpo });
    });

/** Empilha troncos de cone e os une num corpo so. */
function pilha(context is Context, opId is Id, segs is array)
{
    for (var i = 0; i < size(segs); i += 1)
    {
        const s = segs[i];
        const sid = opId + ("s" ~ toString(i));
        const base = vector(0, 0, s[0]) * meter;
        const topo = vector(0, 0, s[1]) * meter;
        if (s[2] == s[3])
        {
            fCylinder(context, sid, { "bottomCenter" : base, "topCenter" : topo, "radius" : s[2] * meter });
        }
        else
        {
            fCone(context, sid, { "bottomCenter" : base, "topCenter" : topo, "bottomRadius" : s[2] * meter, "topRadius" : s[3] * meter });
        }
    }
    opBoolean(context, opId + "uniao", {
                "tools" : qCreatedBy(opId, EntityType.BODY),
                "operationType" : BooleanOperationType.UNION });
}
