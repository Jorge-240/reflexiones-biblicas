import random
import unicodedata


OLD_TESTAMENT_BOOKS = [
    "Génesis",
    "Éxodo",
    "Levítico",
    "Números",
    "Deuteronomio",
    "Josué",
    "Jueces",
    "Rut",
    "1 Samuel",
    "2 Samuel",
    "1 Reyes",
    "2 Reyes",
    "1 Crónicas",
    "2 Crónicas",
    "Esdras",
    "Nehemías",
    "Ester",
    "Job",
    "Salmos",
    "Proverbios",
    "Eclesiastés",
    "Cantares",
    "Isaías",
    "Jeremías",
    "Lamentaciones",
    "Ezequiel",
    "Daniel",
    "Oseas",
    "Joel",
    "Amós",
    "Abdías",
    "Jonás",
    "Miqueas",
    "Nahúm",
    "Habacuc",
    "Sofonías",
    "Hageo",
    "Zacarías",
    "Malaquías",
]

NEW_TESTAMENT_BOOKS = [
    "Mateo",
    "Marcos",
    "Lucas",
    "Juan",
    "Hechos",
    "Romanos",
    "1 Corintios",
    "2 Corintios",
    "Gálatas",
    "Efesios",
    "Filipenses",
    "Colosenses",
    "1 Tesalonicenses",
    "2 Tesalonicenses",
    "1 Timoteo",
    "2 Timoteo",
    "Tito",
    "Filemón",
    "Hebreos",
    "Santiago",
    "1 Pedro",
    "2 Pedro",
    "1 Juan",
    "2 Juan",
    "3 Juan",
    "Judas",
    "Apocalipsis",
]

BIBLE_BOOK_GROUPS = [
    {"titulo": "Antiguo Testamento", "books": OLD_TESTAMENT_BOOKS},
    {"titulo": "Nuevo Testamento", "books": NEW_TESTAMENT_BOOKS},
]

BIBLE_REFLECTIONS = [
    {"book": "Génesis", "reference": "Génesis 1:1", "verse": "En el principio creó Dios los cielos y la tierra.", "reflection": "La historia de la fe comienza reconociendo que todo tiene su origen en Dios. Recordar al Creador ordena nuestra vida y devuelve propósito cuando el corazón se siente disperso.", "tags": ["origen", "creacion", "proposito"]},
    {"book": "Éxodo", "reference": "Éxodo 14:14", "verse": "Jehová peleará por vosotros, y vosotros estaréis tranquilos.", "reflection": "No toda batalla se gana con fuerza humana. Hay momentos en que la obediencia y la calma son la forma más profunda de confiar en Dios.", "tags": ["batalla", "confianza", "paz"]},
    {"book": "Levítico", "reference": "Levítico 19:18", "verse": "Amarás a tu prójimo como a ti mismo.", "reflection": "La santidad bíblica también se expresa en la manera en que tratamos a otros. Amar bien al prójimo es una señal visible de un corazón rendido al Señor.", "tags": ["amor", "projimo", "santidad"]},
    {"book": "Números", "reference": "Números 6:24", "verse": "Jehová te bendiga, y te guarde.", "reflection": "La bendición de Dios no es solo un deseo hermoso; es una declaración de cuidado. Quien es guardado por el Señor puede caminar con esperanza.", "tags": ["bendicion", "cuidado", "esperanza"]},
    {"book": "Deuteronomio", "reference": "Deuteronomio 31:8", "verse": "Jehová va delante de ti; estará contigo, no te dejará, ni te desamparará.", "reflection": "Dios no envía a sus hijos solos al futuro. Su presencia delante de nosotros transforma la incertidumbre en valentía humilde.", "tags": ["futuro", "presencia", "valentia"]},
    {"book": "Josué", "reference": "Josué 1:9", "verse": "Esfuérzate y sé valiente; no temas ni desmayes.", "reflection": "La valentía bíblica no nace de ignorar el miedo, sino de recordar quién acompaña el camino. Dios fortalece a quien sigue adelante en obediencia.", "tags": ["fortaleza", "animo", "obediencia"]},
    {"book": "Jueces", "reference": "Jueces 6:12", "verse": "Jehová está contigo, varón esforzado y valiente.", "reflection": "A veces Dios ve en nosotros un llamado antes de que nosotros lo entendamos. Su palabra levanta al cansado y le recuerda que aún hay propósito por delante.", "tags": ["llamado", "identidad", "fortaleza"]},
    {"book": "Rut", "reference": "Rut 1:16", "verse": "Tu pueblo será mi pueblo, y tu Dios mi Dios.", "reflection": "La fidelidad de Rut revela que la fe también se muestra en la lealtad y el compromiso. Dios honra a quienes caminan con amor perseverante.", "tags": ["fidelidad", "familia", "compromiso"]},
    {"book": "1 Samuel", "reference": "1 Samuel 16:7", "verse": "El hombre mira lo que está delante de sus ojos, pero Jehová mira el corazón.", "reflection": "Dios no se impresiona con apariencias. Él trabaja profundamente en el interior y forma un carácter que vale más que cualquier reconocimiento externo.", "tags": ["corazon", "identidad", "humildad"]},
    {"book": "2 Samuel", "reference": "2 Samuel 22:31", "verse": "Perfecto es el camino de Dios.", "reflection": "Aunque nuestro entendimiento sea limitado, el camino de Dios no se equivoca. Confiar en su dirección evita que el alma se gobierne solo por impulsos o ansiedad.", "tags": ["camino", "direccion", "confianza"]},
    {"book": "1 Reyes", "reference": "1 Reyes 8:61", "verse": "Sea, pues, perfecto vuestro corazón para con Jehová nuestro Dios.", "reflection": "La integridad delante de Dios consiste en una entrega sincera, no en una apariencia religiosa. Un corazón completo para Él aprende a vivir con coherencia.", "tags": ["integridad", "corazon", "consagracion"]},
    {"book": "2 Reyes", "reference": "2 Reyes 6:16", "verse": "Más son los que están con nosotros que los que están con ellos.", "reflection": "Cuando el temor domina la mirada, olvidamos la ayuda invisible de Dios. La fe abre los ojos para reconocer que el Señor sigue sosteniendo la escena.", "tags": ["temor", "proteccion", "fe"]},
    {"book": "1 Crónicas", "reference": "1 Crónicas 16:11", "verse": "Buscad a Jehová y su poder; buscad su rostro continuamente.", "reflection": "La comunión con Dios no es un acto aislado, sino una búsqueda constante. En su presencia el alma encuentra renovación y dirección.", "tags": ["busqueda", "oracion", "presencia"]},
    {"book": "2 Crónicas", "reference": "2 Crónicas 7:14", "verse": "Si se humillare mi pueblo... y oraren, y buscaren mi rostro.", "reflection": "El arrepentimiento sincero abre espacio para la restauración. Dios responde con gracia a quienes vuelven a Él con humildad verdadera.", "tags": ["arrepentimiento", "oracion", "restauracion"]},
    {"book": "Esdras", "reference": "Esdras 7:10", "verse": "Esdras había preparado su corazón para inquirir la ley de Jehová y para cumplirla.", "reflection": "La Palabra transforma mejor cuando se estudia con disposición de obedecer. La fe madura cuando aprender y vivir van de la mano.", "tags": ["palabra", "estudio", "obediencia"]},
    {"book": "Nehemías", "reference": "Nehemías 8:10", "verse": "El gozo de Jehová es vuestra fuerza.", "reflection": "La fortaleza del creyente no depende solo del ánimo humano. El gozo que nace en Dios sostiene incluso en temporadas de reconstrucción y cansancio.", "tags": ["gozo", "fuerza", "restauracion"]},
    {"book": "Ester", "reference": "Ester 4:14", "verse": "¿Y quién sabe si para esta hora has llegado al reino?", "reflection": "Dios coloca a sus hijos en momentos y lugares con propósito. Aun en escenarios difíciles, nuestra vida puede ser instrumento de preservación y bien.", "tags": ["proposito", "tiempo", "valentia"]},
    {"book": "Job", "reference": "Job 19:25", "verse": "Yo sé que mi Redentor vive.", "reflection": "La fe de Job enseña que incluso el dolor más hondo no cancela la esperanza. Confesar al Redentor en medio de la prueba es un acto de adoración.", "tags": ["dolor", "esperanza", "redentor"]},
    {"book": "Salmos", "reference": "Salmos 23:1", "verse": "Jehová es mi pastor; nada me faltará.", "reflection": "La imagen del Pastor nos recuerda cuidado, dirección y provisión. Quien se deja guiar por Dios aprende a descansar en su fidelidad diaria.", "tags": ["cuidado", "descanso", "provision"]},
    {"book": "Proverbios", "reference": "Proverbios 3:5-6", "verse": "Fíate de Jehová de todo tu corazón, y no te apoyes en tu propia prudencia.", "reflection": "La sabiduría bíblica enseña a confiar en Dios por encima del impulso propio. Rendir la mente al Señor endereza decisiones y caminos.", "tags": ["sabiduria", "decision", "confianza"]},
    {"book": "Eclesiastés", "reference": "Eclesiastés 3:1", "verse": "Todo tiene su tiempo, y todo lo que se quiere debajo del cielo tiene su hora.", "reflection": "La impaciencia suele olvidar que Dios trabaja también en los procesos. Reconocer los tiempos ayuda a vivir con serenidad y discernimiento.", "tags": ["tiempo", "paciencia", "discernimiento"]},
    {"book": "Cantares", "reference": "Cantares 8:7", "verse": "Las muchas aguas no podrán apagar el amor.", "reflection": "El amor verdadero posee una fuerza que resiste pruebas y distancias. En la Biblia, el amor perseverante refleja algo del carácter fiel de Dios.", "tags": ["amor", "fidelidad", "relacion"]},
    {"book": "Isaías", "reference": "Isaías 40:31", "verse": "Los que esperan a Jehová tendrán nuevas fuerzas.", "reflection": "Esperar en Dios no es pasividad, sino dependencia activa. Él renueva al cansado y le da aliento para seguir sin rendirse.", "tags": ["espera", "fuerza", "renovacion"]},
    {"book": "Jeremías", "reference": "Jeremías 29:11", "verse": "Yo sé los pensamientos que tengo acerca de vosotros, pensamientos de paz.", "reflection": "Dios no abandona sus planes de bien aun en tiempos de disciplina o exilio. Su propósito sigue apuntando a esperanza y futuro.", "tags": ["esperanza", "futuro", "paz"]},
    {"book": "Lamentaciones", "reference": "Lamentaciones 3:22-23", "verse": "Por la misericordia de Jehová no hemos sido consumidos; nuevas son cada mañana.", "reflection": "Cada amanecer es testimonio de la misericordia renovada de Dios. Su fidelidad diaria sostiene al corazón que atraviesa el quebranto.", "tags": ["misericordia", "fidelidad", "consuelo"]},
    {"book": "Ezequiel", "reference": "Ezequiel 36:26", "verse": "Os daré corazón nuevo, y pondré espíritu nuevo dentro de vosotros.", "reflection": "Dios no solo corrige conductas; transforma el interior. Su obra más profunda consiste en renovar el corazón para una vida nueva.", "tags": ["nuevo_corazon", "transformacion", "restauracion"]},
    {"book": "Daniel", "reference": "Daniel 6:10", "verse": "Daniel se arrodillaba tres veces al día, y oraba y daba gracias delante de su Dios.", "reflection": "La constancia en la oración forma firmeza en tiempos hostiles. Daniel muestra que la fidelidad diaria prepara al creyente para grandes pruebas.", "tags": ["oracion", "fidelidad", "constancia"]},
    {"book": "Oseas", "reference": "Oseas 6:3", "verse": "Conozcamos, y prosigamos en conocer a Jehová.", "reflection": "La relación con Dios no se agota en un momento emocional. Conocerle es un camino continuo de cercanía, verdad y obediencia.", "tags": ["conocer_a_dios", "crecimiento", "perseverancia"]},
    {"book": "Joel", "reference": "Joel 2:13", "verse": "Convertíos a Jehová vuestro Dios; porque misericordioso es y clemente.", "reflection": "El llamado al arrepentimiento siempre está acompañado de la ternura divina. Dios invita a volver, no para humillar sin salida, sino para restaurar.", "tags": ["conversion", "misericordia", "restauracion"]},
    {"book": "Amós", "reference": "Amós 5:24", "verse": "Corra el juicio como las aguas, y la justicia como impetuoso arroyo.", "reflection": "La fe bíblica no separa adoración y justicia. Dios se agrada de una vida que también busca rectitud, verdad y compasión hacia otros.", "tags": ["justicia", "verdad", "compasion"]},
    {"book": "Abdías", "reference": "Abdías 1:15", "verse": "Cercano está el día de Jehová sobre todas las naciones.", "reflection": "La soberbia humana no permanece para siempre. Recordar el señorío de Dios nos llama a vivir con humildad y responsabilidad.", "tags": ["humildad", "juicio", "senorio"]},
    {"book": "Jonás", "reference": "Jonás 2:9", "verse": "La salvación es de Jehová.", "reflection": "Jonás aprendió en el abismo que la salvación no nace del mérito humano. Dios es quien rescata, corrige y vuelve a dar oportunidad.", "tags": ["salvacion", "gracia", "misericordia"]},
    {"book": "Miqueas", "reference": "Miqueas 6:8", "verse": "¿Qué pide Jehová de ti? Solamente hacer justicia, amar misericordia, y humillarte ante tu Dios.", "reflection": "La voluntad de Dios se expresa con claridad y profundidad. La vida piadosa une humildad, misericordia y justicia práctica.", "tags": ["justicia", "misericordia", "humildad"]},
    {"book": "Nahúm", "reference": "Nahúm 1:7", "verse": "Jehová es bueno, fortaleza en el día de la angustia.", "reflection": "En la angustia no solo necesitamos salida, sino refugio. Dios mismo se presenta como fortaleza segura para los que confían en Él.", "tags": ["angustia", "refugio", "bondad"]},
    {"book": "Habacuc", "reference": "Habacuc 3:19", "verse": "Jehová el Señor es mi fortaleza.", "reflection": "Incluso cuando las circunstancias son inciertas, la fortaleza del creyente permanece en Dios. Él sostiene los pasos sobre terreno difícil.", "tags": ["fortaleza", "crisis", "fe"]},
    {"book": "Sofonías", "reference": "Sofonías 3:17", "verse": "Jehová está en medio de ti, poderoso, él salvará.", "reflection": "La presencia de Dios en medio de su pueblo no es distante ni fría. Él se acerca con poder salvador y con amor que restaura.", "tags": ["presencia", "salvacion", "amor"]},
    {"book": "Hageo", "reference": "Hageo 1:7", "verse": "Meditad bien sobre vuestros caminos.", "reflection": "La fe madura también revisa prioridades. Detenerse ante Dios para evaluar el camino puede abrir espacio para una obediencia más clara.", "tags": ["prioridades", "revision", "obediencia"]},
    {"book": "Zacarías", "reference": "Zacarías 4:6", "verse": "No con ejército, ni con fuerza, sino con mi Espíritu.", "reflection": "La obra de Dios no avanza por mera capacidad humana. Dependencia del Espíritu y obediencia humilde producen fruto duradero.", "tags": ["espiritu", "dependencia", "obra_de_dios"]},
    {"book": "Malaquías", "reference": "Malaquías 3:10", "verse": "Probadme ahora en esto... si no os abriré las ventanas de los cielos.", "reflection": "La fidelidad a Dios toca también la administración de lo que recibimos. Él sigue siendo proveedor para quienes le honran con confianza.", "tags": ["provision", "fidelidad", "confianza"]},
    {"book": "Mateo", "reference": "Mateo 11:28", "verse": "Venid a mí todos los que estáis trabajados y cargados, y yo os haré descansar.", "reflection": "Jesús no llama a los perfectos, sino a los cansados. Su descanso nace de una relación viva en la que Él carga con lo que nosotros no podemos.", "tags": ["descanso", "jesus", "cansancio"]},
    {"book": "Marcos", "reference": "Marcos 10:27", "verse": "Para Dios todo es posible.", "reflection": "Cuando las limitaciones humanas se vuelven evidentes, la fe recuerda que Dios no está encerrado en nuestros cálculos. Su poder sigue abriendo camino.", "tags": ["poder", "imposible", "fe"]},
    {"book": "Lucas", "reference": "Lucas 1:37", "verse": "Nada hay imposible para Dios.", "reflection": "La promesa divina no depende de probabilidades humanas. Con Dios, aun lo que parece cerrado puede convertirse en escenario de su fidelidad.", "tags": ["milagro", "promesa", "confianza"]},
    {"book": "Juan", "reference": "Juan 8:12", "verse": "Yo soy la luz del mundo; el que me sigue, no andará en tinieblas.", "reflection": "Seguir a Cristo es recibir dirección para la vida entera. Su luz no solo informa, también transforma y guía el paso cotidiano.", "tags": ["luz", "jesus", "direccion"]},
    {"book": "Hechos", "reference": "Hechos 1:8", "verse": "Recibiréis poder, cuando haya venido sobre vosotros el Espíritu Santo.", "reflection": "La iglesia nace en dependencia del Espíritu, no de estrategias vacías. Dios sigue capacitando para vivir y testificar con poder santo.", "tags": ["espiritu", "mision", "poder"]},
    {"book": "Romanos", "reference": "Romanos 8:28", "verse": "A los que aman a Dios, todas las cosas les ayudan a bien.", "reflection": "Dios puede tejer bien aun con hilos de dolor y confusión. Esta promesa no niega el sufrimiento, pero afirma que no será inútil en sus manos.", "tags": ["bien", "soberania", "esperanza"]},
    {"book": "1 Corintios", "reference": "1 Corintios 13:13", "verse": "Ahora permanecen la fe, la esperanza y el amor, estos tres; pero el mayor de ellos es el amor.", "reflection": "El amor ocupa el lugar central de una vida verdaderamente espiritual. La madurez cristiana se reconoce menos por ruido y más por amor constante.", "tags": ["amor", "madurez", "esperanza"]},
    {"book": "2 Corintios", "reference": "2 Corintios 12:9", "verse": "Bástate mi gracia; porque mi poder se perfecciona en la debilidad.", "reflection": "La gracia de Dios no siempre elimina la debilidad, pero la llena de sentido y poder. Donde somos frágiles, Cristo puede mostrarse suficiente.", "tags": ["gracia", "debilidad", "poder"]},
    {"book": "Gálatas", "reference": "Gálatas 5:1", "verse": "Estad, pues, firmes en la libertad con que Cristo nos hizo libres.", "reflection": "La libertad en Cristo no es licencia para el ego, sino una vida liberada del yugo del pecado para servir con amor y verdad.", "tags": ["libertad", "cristo", "firmeza"]},
    {"book": "Efesios", "reference": "Efesios 2:10", "verse": "Somos hechura suya, creados en Cristo Jesús para buenas obras.", "reflection": "La identidad del creyente nace de la obra de Dios y conduce al servicio. Hemos sido formados con intención, valor y misión.", "tags": ["identidad", "obras", "proposito"]},
    {"book": "Filipenses", "reference": "Filipenses 4:6-7", "verse": "Por nada estéis afanosos... y la paz de Dios guardará vuestros corazones.", "reflection": "La ansiedad no se vence solo con esfuerzo mental; se lleva a Dios en oración. Su paz protege el interior incluso antes de que cambien las circunstancias.", "tags": ["ansiedad", "oracion", "paz"]},
    {"book": "Colosenses", "reference": "Colosenses 3:15", "verse": "La paz de Dios gobierne en vuestros corazones.", "reflection": "Cuando la paz de Dios gobierna, el corazón deja de ser dominado por impulsos y temores. Cristo trae orden interior a la vida diaria.", "tags": ["paz", "corazon", "cristo"]},
    {"book": "1 Tesalonicenses", "reference": "1 Tesalonicenses 5:16-18", "verse": "Estad siempre gozosos. Orad sin cesar. Dad gracias en todo.", "reflection": "La vida cristiana se alimenta de gozo, oración y gratitud continuos. Estas prácticas mantienen el corazón sensible a la presencia de Dios.", "tags": ["gozo", "gratitud", "oracion"]},
    {"book": "2 Tesalonicenses", "reference": "2 Tesalonicenses 3:3", "verse": "Fiel es el Señor, que os afirmará y guardará del mal.", "reflection": "Nuestra seguridad última no descansa en vigilancia humana, sino en la fidelidad del Señor. Él afirma y guarda a los suyos.", "tags": ["fidelidad", "proteccion", "seguridad"]},
    {"book": "1 Timoteo", "reference": "1 Timoteo 4:12", "verse": "Sé ejemplo de los creyentes en palabra, conducta, amor, espíritu, fe y pureza.", "reflection": "El testimonio cristiano alcanza cada área de la vida. La fe se vuelve visible cuando palabra y conducta caminan juntas.", "tags": ["testimonio", "pureza", "ejemplo"]},
    {"book": "2 Timoteo", "reference": "2 Timoteo 1:7", "verse": "No nos ha dado Dios espíritu de cobardía, sino de poder, de amor y de dominio propio.", "reflection": "El temor no tiene la última palabra en la vida del creyente. Dios concede fortaleza interior, amor y dominio para caminar con firmeza.", "tags": ["temor", "dominio_propio", "poder"]},
    {"book": "Tito", "reference": "Tito 2:11-12", "verse": "La gracia de Dios... nos enseña que, renunciando a la impiedad, vivamos en este siglo sobria, justa y piadosamente.", "reflection": "La gracia no solo perdona; también educa. Dios forma una vida sobria y piadosa a partir de su favor inmerecido.", "tags": ["gracia", "santidad", "vida_piadosa"]},
    {"book": "Filemón", "reference": "Filemón 1:16", "verse": "No ya como esclavo, sino como más que esclavo, como hermano amado.", "reflection": "El evangelio transforma relaciones rotas en fraternidad. En Cristo, la dignidad y la reconciliación toman un lugar central.", "tags": ["reconciliacion", "dignidad", "hermandad"]},
    {"book": "Hebreos", "reference": "Hebreos 12:2", "verse": "Puestos los ojos en Jesús, el autor y consumador de la fe.", "reflection": "La perseverancia cristiana se fortalece cuando la mirada permanece en Cristo. Él inicia, sostiene y completa la fe de su pueblo.", "tags": ["jesus", "perseverancia", "fe"]},
    {"book": "Santiago", "reference": "Santiago 1:5", "verse": "Si alguno de vosotros tiene falta de sabiduría, pídala a Dios.", "reflection": "Dios no desprecia la necesidad honesta de dirección. La sabiduría pedida con fe orienta decisiones, relaciones y tiempos difíciles.", "tags": ["sabiduria", "peticion", "direccion"]},
    {"book": "1 Pedro", "reference": "1 Pedro 5:7", "verse": "Echando toda vuestra ansiedad sobre él, porque él tiene cuidado de vosotros.", "reflection": "La ansiedad se vuelve más ligera cuando se entrega a quien realmente cuida. Dios invita a depositar el peso del corazón en sus manos.", "tags": ["ansiedad", "cuidado", "confianza"]},
    {"book": "2 Pedro", "reference": "2 Pedro 3:18", "verse": "Creced en la gracia y el conocimiento de nuestro Señor y Salvador Jesucristo.", "reflection": "La fe sana no se estanca. Dios nos llama a un crecimiento continuo en gracia y conocimiento de Cristo.", "tags": ["crecimiento", "gracia", "conocimiento"]},
    {"book": "1 Juan", "reference": "1 Juan 4:19", "verse": "Nosotros le amamos a él, porque él nos amó primero.", "reflection": "El amor cristiano no nace del vacío; responde al amor primero de Dios. Esta verdad sana la identidad y renueva la manera de relacionarnos.", "tags": ["amor", "identidad", "dios"]},
    {"book": "2 Juan", "reference": "2 Juan 1:6", "verse": "Este es el amor, que andemos según sus mandamientos.", "reflection": "El amor bíblico no es solo emoción sincera; también es obediencia. Caminar en la verdad honra al Dios que amamos.", "tags": ["amor", "obediencia", "verdad"]},
    {"book": "3 Juan", "reference": "3 Juan 1:4", "verse": "No tengo yo mayor gozo que este, el oír que mis hijos andan en la verdad.", "reflection": "La alegría espiritual más profunda aparece cuando la verdad se vuelve vida concreta. Caminar en la verdad bendice a quien guía y a quien aprende.", "tags": ["verdad", "gozo", "discipulado"]},
    {"book": "Judas", "reference": "Judas 1:21", "verse": "Conservaos en el amor de Dios.", "reflection": "Permanecer en el amor de Dios exige vigilancia espiritual y dependencia continua. La perseverancia se nutre de una relación viva con Él.", "tags": ["amor_de_dios", "perseverancia", "vigilancia"]},
    {"book": "Apocalipsis", "reference": "Apocalipsis 21:5", "verse": "He aquí, yo hago nuevas todas las cosas.", "reflection": "La historia bíblica termina con esperanza renovadora. Dios no solo remienda el mundo; promete una restauración completa bajo su gloria.", "tags": ["esperanza", "restauracion", "nuevas_todas_las_cosas"]},
]


def _normalize(text: str) -> str:
    base = unicodedata.normalize("NFKD", (text or "").lower())
    return "".join(ch for ch in base if not unicodedata.combining(ch))


def select_bible_reflection(used_references: set[str], query: str | None = None) -> dict | None:
    normalized_query = _normalize(query or "")
    pool = [item for item in BIBLE_REFLECTIONS if item["reference"] not in used_references]
    if not pool:
        return None

    if normalized_query:
        filtered = []
        for item in pool:
            searchable = " ".join([item["book"], item["reference"], item["verse"], " ".join(item["tags"])])
            if normalized_query in _normalize(searchable):
                filtered.append(item)
        if filtered:
            pool = filtered

    return random.choice(pool)
