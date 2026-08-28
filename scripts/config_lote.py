"""Config por vídeo do lote jul/ago 2026. Estilo aprovado no VID8 (Dorflex)."""

# excluir: trechos de take abortado / falso início (segundos no bruto)
# escada: (texto_condensado, primeira_palavra_do_degrau) -> vira escadinha
# destaques: (frase_ancora, {palavras_chave}) -> destaque inline bold ciano
CONFIG = {
 "VID4": {
   "excluir": [(7.4, 10.05)],                      # "Esse mes-- medo,"
   "escada": [("medicação certa","medicação"),("fisioterapia","fisioterapia"),
              ("fortalecimento","fortalecimento"),("infiltração","infiltração")],
   "destaques": [("exceção",{"exceção"}), ("minoria",{"minoria"}), ("maioria",{"maioria"}),
                 ("necessária",{"necessária"}), ("adiar",{"adiar"})],
 },
 "VID5": {
   "excluir": [],
   "escada": [("movimento na dose certa","movimento"),("fortalecimento","fortalecimento"),
              ("ajuste de postura","ajuste"),("atividade orientada","atividade")],
   "destaques": [("enfraquecer",{"enfraquecer"}), ("rígida",{"rígida"}),
                 ("contrário",{"contrário"}), ("avaliação",{"avaliação"})],
 },
 "VID7": {
   # gagueira "pre--" antes de "existem"
   "excluir": [(25.50, 25.71)],
   "escada": [("perda de força","Um"),("dormência","Dois"),
              ("dificuldade pra urinar","Três"),("dor que piora à noite","quatro")],
   "destaques": [("quatro sinais",{"quatro"}), ("ignoram",{"ignoram"}),
                 ("rápida",{"rápida"}), ("Salva",{"salva"})],
 },
 "VID10": {
   "excluir": [],
   "escada": [("tela baixa","um"),("longe do encosto","dois"),("mesma posição","três")],
   "destaques": [("três erros",{"três"}), ("rigidez",{"rigidez"}),
                 ("Ergonomia",{"ergonomia"}), ("causa",{"causa"})],
 },
 "VID11": {
   "excluir": [(13.2, 14.05)],                     # "Agora," pendurado
   "escada": [],
   "destaques": [("adaptação normal",{"adaptação"}), ("aviso",{"aviso"}),
                 ("lesão",{"lesão"}), ("sem abandonar",{"abandonar"})],
 },
 "VID13": {
   "excluir": [(30.2, 34.3)],                      # take abortado "e se você--"
   "escada": [("fisioterapia específica","fisioterapia"),("correção de postura","correção"),
              ("infiltração guiada","infiltração")],
   "destaques": [("hérnia de disco cervical",{"cervical"}), ("remédio forte",{"forte"}),
                 ("tratar a causa",{"causa"})],
 },
 "VID15": {
   "excluir": [(24.6, 38.7)],                      # take abortado + "Peraí"
   "escada": [],
   "destaques": [("não precisa operar",{"operar"}), ("conservador",{"conservador"}),
                 ("necessário",{"necessário"}), ("Me segue",{"segue"})],
 },
 "VID16": {
   "excluir": [],
   "escada": [],
   "destaques": [("não é normal",{"normal"}), ("frescura",{"frescura"}),
                 ("sobrecarga",{"sobrecarga"}), ("crônica",{"crônica"}), ("alerta",{"alerta"})],
 },
 "VID17": {
   "excluir": [(22.9, 33.3)],                      # take abortado "mas parar..."
   "escada": [("controle da dor","controle"),("fortalecimento progressivo","fortalecimento"),
              ("retorno por etapas","retorno")],
   "destaques": [("ansiedade",{"ansiedade"}), ("evolui bem",{"bem"}),
                 ("plano próprio",{"próprio"}), ("raramente",{"raramente"})],
 },
}
