FeatureScript 3112;
import(path : "onshape/std/geometry.fs", version : "3112.0");

// MarsMission - VERIFICACAO geometrica do modelo (Etapa 7.2b), nao validacao. ARQUIVO GERADO por tools/encaixe_coifas.py a
// partir de cad/featurescript/envelope.fs e de results/: nao editar a mao. Este modelo nao tem nenhuma dimensao.
// Envelope: leitura da figura "Simplified" [F80] Fig. 4.3.1-1, p. 4-8, nao e dado do fabricante em CAD. Plano: "LV STA 2596.66 (1575 Interface)".
// O envelope e uma casca fina e sem material: a face INTERNA e o limite do volume utilizavel, e a espessura nao tem sentido
// fisico. Com uma casca, Check interference so acusa o que atravessa o limite; um solido acusaria o veiculo inteiro.
// Eixos: z = altura acima do plano da interface. Segmentos em metros: [z0, z1, r0, r1].

export enum LeituraEnvelope
{
    annotation { "Name" : "Contorno reto entre as cotas" }
    L0,
    annotation { "Name" : "Diametro menor desde o plano da interface" }
    L1
}
const OPCOES = [LeituraEnvelope.L0, LeituraEnvelope.L1];
const SEGMENTOS = [
    { "interno" : [[-0.137, -0.127, 2.4385, 2.4385], [-0.127, 6.477, 2.4385, 2.324], [6.477, 9.271, 2.324, 1.816], [9.271, 12.6746, 1.816, 0.419]], "externo" : [[-0.127, 6.477, 2.4485, 2.334], [6.477, 9.271, 2.334, 1.826], [9.271, 12.6746, 1.826, 0.429], [12.6746, 12.6846, 0.429, 0.429]] },
    { "interno" : [[-0.137, -0.127, 2.324, 2.324], [-0.127, 6.477, 2.324, 2.324], [6.477, 9.271, 2.324, 1.816], [9.271, 12.6746, 1.816, 0.419]], "externo" : [[-0.127, 6.477, 2.334, 2.334], [6.477, 9.271, 2.334, 1.826], [9.271, 12.6746, 1.826, 0.429], [12.6746, 12.6846, 0.429, 0.429]] }
];
const NOME = "Envelope Vulcan VC4 (referencia, sem material)";
const COR = [0.15, 0.55, 0.85, 0.25];
const Z_INTERFACE = 0;

annotation { "Feature Type Name" : "MarsMission envelope Vulcan" }
export const marsMissionEnvelopeVulcan = defineFeature(function(context is Context, id is Id, definition is map)
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
