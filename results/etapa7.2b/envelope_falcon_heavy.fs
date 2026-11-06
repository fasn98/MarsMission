FeatureScript 3112;
import(path : "onshape/std/geometry.fs", version : "3112.0");

// MarsMission - VERIFICACAO geometrica do modelo (Etapa 7.2b), nao validacao. ARQUIVO GERADO por tools/encaixe_coifas.py a
// partir de cad/featurescript/envelope.fs e de results/: nao editar a mao. Este modelo nao tem nenhuma dimensao.
// Envelope: perfil amostrado do STEP de keep-in do fabricante [F82] p. 16, Tab. 4-1. Plano: origem do arquivo, premissa P-096.
// O envelope e uma casca fina e sem material: a face INTERNA e o limite do volume utilizavel, e a espessura nao tem sentido
// fisico. Com uma casca, Check interference so acusa o que atravessa o limite; um solido acusaria o veiculo inteiro.
// Eixos: z = altura acima do plano da interface. Segmentos em metros: [z0, z1, r0, r1].

export enum LeituraEnvelope
{
    annotation { "Name" : "Keep-in do fabricante, faixas de 500 mm" }
    L0
}
const OPCOES = [LeituraEnvelope.L0];
const SEGMENTOS = [
    { "interno" : [[-0.01, 0, 2.323, 2.323], [0, 0.5, 2.323, 2.3201], [0.5, 1, 2.3201, 2.316], [1, 1.5, 2.316, 2.3118], [1.5, 2, 2.3118, 2.3077], [2, 2.5, 2.3077, 2.3035], [2.5, 3, 2.3035, 2.2994], [3, 3.5, 2.2994, 2.2953], [3.5, 4, 2.2953, 2.2911], [4, 4.5, 2.2911, 2.287], [4.5, 5, 2.287, 2.2827], [5, 5.5, 2.2827, 2.2787], [5.5, 6, 2.2787, 2.2745], [6, 6.5, 2.2745, 2.2704], [6.5, 7, 2.2704, 2.2606], [7, 7.5, 2.2606, 2.2099], [7.5, 8, 2.2099, 2.1051], [8, 8.5, 2.1051, 1.9619], [8.5, 9, 1.9619, 1.7996], [9, 9.5, 1.7996, 1.5966], [9.5, 10, 1.5966, 1.3356], [10, 10.5, 1.3356, 1.0023], [10.5, 11, 1.0023, 0.5787], [11, 11.3476, 0.5787, 0.005]], "externo" : [[0, 0.5, 2.333, 2.3301], [0.5, 1, 2.3301, 2.326], [1, 1.5, 2.326, 2.3218], [1.5, 2, 2.3218, 2.3177], [2, 2.5, 2.3177, 2.3135], [2.5, 3, 2.3135, 2.3094], [3, 3.5, 2.3094, 2.3053], [3.5, 4, 2.3053, 2.3011], [4, 4.5, 2.3011, 2.297], [4.5, 5, 2.297, 2.2927], [5, 5.5, 2.2927, 2.2887], [5.5, 6, 2.2887, 2.2845], [6, 6.5, 2.2845, 2.2804], [6.5, 7, 2.2804, 2.2706], [7, 7.5, 2.2706, 2.2199], [7.5, 8, 2.2199, 2.1151], [8, 8.5, 2.1151, 1.9719], [8.5, 9, 1.9719, 1.8096], [9, 9.5, 1.8096, 1.6066], [9.5, 10, 1.6066, 1.3456], [10, 10.5, 1.3456, 1.0123], [10.5, 11, 1.0123, 0.5887], [11, 11.3476, 0.5887, 0.015], [11.3476, 11.3576, 0.015, 0.015]] }
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
