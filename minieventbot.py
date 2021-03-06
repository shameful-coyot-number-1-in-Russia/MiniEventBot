from flask import Flask, request, json
from bs4 import BeautifulSoup as BS
import wikipedia
import requests
import vk_api
import random

question_aarray=["0.Что тебе не понятно в фразе от 1 до 300?", "1.Любимый цвет?","2.Любимый фильм?","3.Любимый актер (актриса)?", "4.Любимая песня?","5.Любимая книга?","6.Любимое стихотворение?","7.Любимый цветок?","8.Любимое животное?","9.Любимая птица?","10.Любимое дерево?",
                 "11.Какой бы ты хотел подарок получить?","12.Любимая страна?","13.Любимый город?","14.Любимый школьный год?","15.Любимый учитель?","16. Любимая машина?","17.Любимое мужское имя?","18.Любимое женское имя?","19.Любимая еда?","20.Любимый десерт?",
                 "21.Любимый напиток?", "22.Любимая часть тела?", "23.Любимая одежда?","24.Любимый спорт?","25.Любимое число?","26.Любимая телевизионная программа?","27. Время года?","28.Любимый день недели?", "29.Любимое время суток?","30.Любимый праздник?",
                 "31.Любимое высказывание?","32.Любимый танец?","33.Любимый член семьи?","34.Любимый парфюм?","35.Любимое развлечение?","36. Где ты родился(ась)?","37. Где ты жил(а) в детстве?","38. Какая была любимая игра дома и какая на улице?","39. С кем ты проводил(а) большую часть своего времени?","40. Какой наиболее запоминающийся момент из детства?",
                 "41. Каким был твой самый большой страх (темноты, чудовищ и пр.)?","42. Кем в детстве ты мечтал(а) быть? Это так сейчас? Почему?","43. Какая самая забавная вещь, случившаяся с тобой в детстве?","44. Какая самая щекотливая ситуация, в которую ты попадал(а) в детстве?","45. Каковы знаменательные события детства, которые больше всего повлияли на тебя?","46. Какое твое любимое воспоминание, связанное с мамой?","47. Какое твое любимое воспоминание, связанное с папой?","48. Какой твой любимый школьный класс и почему?","49. Какой твой самый любимый школьный предмет?","50. Какой твой самый нелюбимый школьный предмет?",
                 "51. Какая у тебя была любимая игрушка?","52. Кто был твоим(ей) лучшим другом (подругой)?","53. Какую игрушку ты всегда хотел(а), но так и не получил(а)?","54. Какие у тебя были самые лучшие летние каникулы?","55. Какое животное более всего соответствует тебе?","56. Если бы у тебя была возможность выбрать любую в мире работу, то какой бы она была?","57. Что бы ты изменил(а) в прошлом, если бы была такая возможность?","58. Если бы ты выиграл(а) в лотерею миллион долларов, куда бы потратил(а) деньги?","59. Какой мультипликационный персонаж наиболее близок тебе и почему?","60. Чему бы ты хотел(а) посвятить свою жизнь?",
                 "61. Если бы была возможность прямо сейчас избавиться от какой-нибудь привычки, от чего ты бы избавился(лась)?","62. Если бы у тебя была одна магическая способность, какой бы она была?","63. Какими тремя вещами ты больше всего в жизни гордишься?","64. Какими тремя словами наиболее полно ты можешь описать себя?","65. Чего ты больше всего боишься?","66. Что ты делаешь, когда тебе грустно?","67. Что ты делаешь, когда чувствуешь злость или расстройство?","68. Относишься ли ты к какой-нибудь религии?","69. Веришь ли ты в судьбу?","70. Веришь ли в любовь с первого взгляда?",
                 "71. Что больше всего привлекает в женщинах (мужчинах?)","72. В чем для тебя различие между любовью и влюбленностью?","73. Как ты считаешь, можно ли выражать свои чувства на людях? И до какой степени можно?","74. Ты веришь в Бога?","75. Ты веришь в загробную жизнь?","76. Как ты думаешь откуда произошел человек?","77. Есть ли жизнь на других планетах?","78. Что ты думаешь по поводу абортов?","79. Должны ли дети, когда вырастают жить вместе с родителями?","80. Какое твое отношение к геям и лесбиянкам?",
                 "81. Как ты относишься к гаремам?","82. Как ты относишься к разнице в возрасте между мужчиной и женщиной (разница более 10 лет)?","83. Достаточно ли для счастья только любви? И возможен ли «рай в шалаше»?","84. Должен ли мужчина присутствовать при рождении ребенка?","85. Может ли время вылечить любовные раны?","86. Какой он дом твоей мечты?","87. Какая она машина твоей мечты?","88. Идеальные каникулы или выходные. Какие они?","89. Каким должен быть идеальный День Рождения?","90. Какая мечта всей твоей жизни?",
                 "91. Три черты или свойства тебя, которые ты хотел(а) бы улучшить?","92. Какие пять вещей/дел ты бы хотел","93.Твое любимое аниме?","94.Твой любимый чай","95. Ты предпочитаешь жару или холод? Почему?","96. Ты сова или жаворонок?","97. Что тебя больше всего раздражает?","98. Тебе больше нравятся кошки или собаки?","99. Ты живешь сегодняшним днем или будущим?","100. Твое отношение к курению?",
                 "101. Сплетни и слухи… нравятся / не нравятся?","102. Сюрпризы … нравятся / не нравятся?","103. Тихие и спокойные местечки… нравятся / не нравятся?","104. Шумные места… нравятся / не нравятся?","105. Амбиции… нравятся / не нравятся?","106. Соперничество… нравится / не нравится?","107. Преимущества мужчины в любви","108. Преимущества женщины в любви","109. Мужчина был бы лучшим «правителем земли», потому что…","110. Женщина была бы лучшим «правителем земли», потому что…",
                 "111. Самый большой страх мужчины","112. Самый большой страх женщины","113. Что всем мужчинам нравится слышать в свой адрес…","114. Что всем женщинам нравится слышать в свой адрес…","115. Лучший довод, чтобы быть мужчиной","116. Лучший довод, чтобы быть женщиной","117. Самый большой минус быть мужчиной","118. Самый большой минус быть женщиной","119. Если бы у тебя была возможность родиться второй раз и возможность выбрать свой пол, кем бы ты был(а)?","120. Как ты представляешь себе идеальное свидание?",
                 "121. Какой твой любимый романтический жест или поступок?","122. Десять подарков, которые бы ты больше всего на свете хотел(а) получить?","123. Как ты представляешь себе идеальный романтический подарок?","124. Как ты представляешь себе идеальные романтические выходные или каникулы?","125. Какими способами я могу тебя поддержать в трудные для тебя минуты?","126. Что такого необычного и уникального ты находишь в наших взаимоотношениях?","127. Ты считаешь себя романтичным(ой)?","128. Что для тебя настоящая Любовь?","129. Ты веришь в родство душ и что у каждого человека есть своя половинка на этой земле?","130. Романтика это важная часть взаимоотношений?",
                 "131. Как ты думаешь, может ли настоящая Любовь победить все?","132. Вы помните в деталях вашу первую встречу с любым из участников беседы? Ваши мысли в это время?","133. Вы помните в деталях ваше первое свидание с любым из участников беседы? Ваши мысли в это время?","134. Вы помните ваш первый поцелуй с любым участником беседы? Что вы чувствовали и о чем думали?","135. Когда вы осознали, что любите друг друга(с своей второй половинкой) (кто первый осознал, или одновременно?)","136. Вы помните вашу первую ссору (вашу самую крупную ссору)? Что вы о ней думаете сейчас? Могла бы ли она повториться?","137. Вы помните самый потрясающий комплимент, который сказал вам ваш партнер?","138. Какие свойства характера и личности вам больше всего нравятся в вашем партнере?","139. Какие три вещи вы можете сделать, чтобы ваши взаимоотношения стали лучше? (так постарайтесь сделать их!)","140. Как изменилась ваша жизнь с тех пор, как вы встретили друг друга. Что изменилось в вас самих к лучшему?",
                 "141. Что больше всего вы цените в том, что делает для вас ваш партнер?","142. Как ваши различия дополняют друг друга?","143. Что вы делали, чтобы привлечь внимание вашего партнера до того, как у вас начались серьезные взаимоотношения?","144. Вам нравится, когда любимый вами человек делает…","145. Вам нравится, когда любимый вами человек называет вас…","146. Самая романтичная ситуация между вами","147. Как вы считаете, ваша жизнь стала предсказуемой?","148. Что нужно делать, чтобы внести в жизнь разнообразие?","149. Почему вы хотите и дальше быть вместе?","150. Секс до свадьбы. Твое отношение к нему? Твое отношение к эгоизму в сексе?",
                 "151. Следует ли жить вдвоем до свадьбы?","152. Следует ли всегда говорить правду, даже если она причиняет боль?","153. Для чего люди женятся? * Зачем тебе замуж?","154. Ты веришь в брак на всю жизнь? Твое отношение к разводам?","155. Самая важная вещь во взаимоотношениях?","156. Ты можешь свободно спросить меня о чем хочешь?","157. Какой должна быть роль жены в семье? *Семейные обязанности*  какие?","158. Какой должна быть роль мужа в семье?","159. Если бы ты мог(ла) изменить что-нибудь в нашей совместной жизни, то что это было бы?","160. Если ты недоволен(льна) или рассержен(на) чем-то, как ты это демонстрируешь? И как мне понять чем именно?",
                 "161. Если у тебя проблемы, ты об этом говоришь открыто или держишь в себе?","162. Тебе нравится рассказывать о своих чувствах?","163. Как ты относишься к моим друзьям противоположного пола?","164. Как ты относишься к моим прошлым любвям(что не так с этим вопросом ахахахахах)?","165. Что бы ты делал(а), если бы выяснилось, что любимый человек обманывает тебя?","166. В каком случае возможен развод?","167. В семье кто должен распоряжаться деньгами?","168. Следует ли жене (мужу) сидеть дома с детьми?","169. Как ты относишься к женщине, которая зарабатывает больше мужчины (достигла большего в карьере)?","170. Как ты думаешь, стоит ли экономить?",
                 "171. Стоит ли иногда потранжирить деньги?","172. От чего бы ты смог(ла) отказаться, чтобы сэкономить деньги?","173. Что бы ты делал(а), если бы твой партнер оказался временно не способным зарабатывать деньги? А если бы долго не мог устроиться на работу?","174. Хочешь ли ты детей?","175. Если да, то сколько детей хочешь? Какого пола? Как назвать?","176. Как бы ты воспитывал(а) детей? Как твои родители или по-другому?","177. Ты бы наказывал(а) детей? Если да, то как и за что?","178. Какова роль мамы в воспитании детей?","179. Какова роль папы в воспитании детей?","180. Какова возможна роль бабушки и дедушки в воспитании ваших детей?",
                 "181. Мужчина и женщина любят друг друга меньше после рождения ребенка?","182. Не считаешь ли ты, что рождение ребенка ставит крест на нашей жизни только друг для друга?","183. Можно ли ссориться на глазах у детей?","184. Можно ли показывать любовь друг к другу на глазах у детей? Где граница?","185. Как бы ты ответил(а) на вопрос ребенка: «Откуда берутся дети?»","186. Как можно продолжать наши романтические встречи и свидания, когда у нас будут дети?","187. Что бы ты рассказал(а) детям об алкоголе, курении и наркотиках?","188. Секс это важно, чтобы быть счастливой парой?","189. В чем различие между «заниматься сексом» и «заниматься любовью»?","190. Какой аспект ваших сексуальных взаимоотношений вы бы хотели улучшить?",
                 "191. Вы чувствуете себя 100% комфортно в вашей сексуальной жизни? Почему да или почему нет?","192. Насколько важно для вас сексуальное прошлое вашего партнера?","193. Вы думаете, что знаете все о сексуальных желаниях вашего партнера?","194. Как вы думаете, разнообразие в сексе важно для длительных взаимоотношений?","195. Какая ваша любимая *прелюдия?","196. Какой ваш любимый поцелуй?","197. Какая ваша любимая сексуальная позиция?","198. Как вам больше нравится, чтобы к вам прикасались, гладили, ласкали?","199. Как вам больше всего нравится ласкать партнера?","200. Какая ваша самая секретная сексуальная фантазия?",
                 "201. Где вам больше всего нравится заниматься любовью?","202. А в каком самом необычном месте вы занимались любовью?","203. Какая музыка вам больше всего нравится, чтобы играла, когда вы занимаетесь любовью?","204. В какое время дня вам нравится заниматься любовью?","205. Что вам нравится делать после занятий любовью?","206. Как вы думаете, от кого должна исходить инициатива, от мужчины или от женщины? А как по поводу скрытой инициативы?","207. Что вас наиболее возбуждает в вашем партнере?","208. Если бы у вас была возможность что-либо изменить в вашей сексуальной жизни, что бы это было?","209.Что ты чувствуешь, когда обнимаешь меня?","210. Что ты чувствуешь, когда я опаздываю, и тебе приходится меня ждать?",
                 "211.ЧТо ты чувствуешь, когда ты опаздываешь, и мне приходится тебя ждать?", "212.Что ты чувствуешь, когда я убеждаю тебя в чем-то, а ты не хочешь с этим согласиться?","213.Что ты ччувствуешь, когда ты хвалишь меня или говоришь мне комплимент?","214. Какой тебе дарили самый странный подарок?","215. Какое ты видела самое интересное произведение искусства? ","216. Что наделяет твою жизнь смыслом? ","217. Какие самые важные три вещи необходимо сделать в жизни? ","218. Ты веришь, что любовь может длиться всю жизнь?","219. Что ты больше любишь: готовить или есть? ","220. Что ты предпочитаешь больше: чай или кофе? ",
                 "221. Какой твой любимый десерт? ","222. Какие твои любимые цветы?","223. О чем ты никогда не рассказывала своим родителям?","224. Как бы ты описала себя с помощью одного предложения? ","225. Какой был самый трудный момент в твоей жизни?","226. Какой самый ценный жизненный урок ты получила от своих родителей? ","227. Что ты никогда не простишь своему парню и своей лучшей подруге? ","228. Что бы ты сделала, если была бы уверена, что никто тебя не накажет и не осудит?","229. Ты хотела бы иметь такого друга, как ты?","230. Ты легко отпускаешь ненужных людей и негативные эмоции?",
                 "231. За что ты больше всего благодарна своей жизни?","232. Какое самое большое поражение ты претерпела на своем жизненном пути?","233. Что тебе приходится делать из того, что ты не любишь? ","234. Как ты считаешь, есть ли польза от страданий? ","235. За какой совершенный поступок тебе стыдно? ","236. О каком интересном факте, связанном с тобой, большинство окружающих не знает?","237. Какое было самое лучшее решение из принятых тобой за все время?","238. Когда ты последний раз обманывала?","239. Когда последний раз ты вышла из себя?","240. Если у тебя возникнет 1 час свободного времени, чем займешься? ",
                 "241. На чью жизнь ты оказала сильное влияние?","242. Ты когда-нибудь прогуливалась без зонта под дождем?","243. Ты когда-нибудь прыгала с парашютом?","244. Случалось ли с тобой, чтобы ты находила кошелек с деньгами?","245. У тебя есть татуировки?","246. Тебе доводилось повстречать знаменитость?","247. Ты когда-нибудь играла в “Дурака” на раздевание?","248. Ты когда-либо шпионила за своими соседями?","249. Тебе приходилось выступать на сцене?","250. Ты участвовала в каком-нибудь конкурсе или соревновании?",
                 "251. О чем ты любишь думать в свободное время?","252. Какое качество в себе ты ценишь больше всего?","253. Какое в тебе есть отрицательное качество?","254. Какую черту характера в человеке ты считаешь самой благородной?","255. Какую черту характера в человеке ты считаешь самой низменной?","256. Ты сожалеешь о чем-нибудь, что ты совершил(а) в прошлом?","257. Если бы была возможность, согласился(ась) ли изменить события прошлого? Если да, то как по-новому ты бы себя повел(а)?","258. Если бы ты писал(а) книгу о себе, какой у нее был бы заголовок?","259. Если бы тебе пришлось провести целый день в одиночку, чем бы ты занялся(ась)?","260. Твоя самая худшая ситуация на работе?",
                 "261. Твоя самая лучшая ситуация на работе?","262. Что тебя раздражает?","263. Если бы ты смог(ла) изменить одну вещь в мире, что это за вещь была бы?","264. Что бы положительного ты бы добавил(а) в мир?","265. Что бы отрицательного ты бы убрал(а) из мира?","266. Что бы ты хотел(а) владеть собственной компанией или работать на кого-либо?","267. Насколько для тебя важна карьера?","268. Насколько для тебя важна семья?","269. Как ты поднимаешь себе настроение, если чем-то расстроен(а)?","270. Ты считаешь что твоя жизнь идет так, как тебе хотелось бы?",
                 "271. На сколько бы ты оценил(а) свои достижения в жизни?","272. Как ты себя чувствуешь, когда приходится говорить публично?","273. Что ты думаешь о существующем правительстве в стране?","274. Как ты думаешь, цель оправдывает средства?","275. Какой самый страшный кошмар тебе снился?","276. Какой самый лучший сон тебе снился?","277. Какой самый страшный момент в жизни у тебя был?","278. Как ты оцениваешь твое взаимоотношение с родителями?","279. Ты согласен(на) с тем, как воспитывали тебя твои родители?","280. Если бы у тебя была возможность родиться в другой стране, что это была бы за страна?",
                 "281. Где бы ты хотел(а) жить в городе или в деревне?","282. Какой твой астрологический знак? Как ты думаешь, его описание подходит к тебе? Насколько это правда?","283. Как ты думаешь зачем придумали астрологию? Почему?","284. Как ты воспринимаешь людей, как «потенциально добрых» или «потенциально плохих»?","285. Ты экстраверт или интроверт?","286. Ты сангвиник, холерик, флегматик или меланхолик? ","287. Ты бы хотел(а) иметь много друзей или небольшой круг очень близких друзей?","288. Как тебе больше всего нравится проводить праздники?","289. Кто в жизни на тебя повлиял больше всего?","290. Какой твой самый важный жизненный урок, который бы ты хотел, чтобы знали все?",
                 "291. Если бы ты мог(ла) изменить свое имя, то на какое?","292. Что ты больше всего ценишь в подарке?","293. 10 моментов из автобиографии, наиболее полно описывающих твою личность?","294. Нравится ли тебе отвечать на вопросы психологических тестов? Почему?","295. Если бы психиатр предложил вам «инъекцию сыворотки правды» путем записи на магнитофон ваших ответов на вопросы о вас самих, ваших подлинных чувствах, мотивах и желаниях, вы бы согласились? Не испытали бы вы двойственного чувства — отчасти любопытства, отчасти страха перед тем, что может обнаружиться в вас?","296. Какая эмоция, о которой тебе труднее всего признаться?","297. Если бы оставалось жить один день, что бы ты сделал? Какие твои чувства?","298. Если бы оставалось жить один месяц, что бы ты сделал? Какие твои чувства?","299. Если бы оставалось жить один год, что бы ты сделал? Какие твои чувства?","300. Хорошо ли мы знаем друг друга?",
                 "301.Какой ты была в детстве? Хулиганкой или спокойной девушкой?","302.Любишь мечтать? О чем мечтаешь?","303.Что тебя больше всего рассмешило за прошедшую неделю/месяч?","304.Ты творческий человек? Почему так считаешь? Если да, то, что играет в роли твоей музы?","305.Что ты выбираешь: Спонтанность или стабильность?","306.Тебе нравится получать подарки, или приятней дарить их?","307.Какой звук тебе нравится? Звук горящего камина в доме, или может звук природы в лесу?","308.Насколько ты считаешь себя собранной? В квартире твоей беспорядок?","309.Веришь в знаки зодиака? Какой твой?","310.Сериалы, которые ты любишь смотреть?",
                 "311.Занимаешься спортом? Каким? Как часто?","312.Веришь в настоящую любовь? Почему?","313.Какой фильм ты можешь смотреть снова и снова?","314.Есть сестра или брат?","315.Нравится танцевать? Почему? Какие танцы нравятся?","316.Жалеешь о чем-нибудь в своей жизни?","317.Сколько языков ты знаешь? Какие хотела бы еще выучить? Почему?","318.Как думаешь романтично будет заняться любовью на берегу моря?","319.Научить тебя делать шашлыки?","320.Ты хочешь остаться такой молодой и красивой навсегда?",
                 "321.Ты обещаешь не врать друг другу никогда?","322.Какое обычно у тебя утром настроение?","323.Что ты подаришь мне на 23 февраля?","324.Как лето проводишь (будешь проводить)?","325.Хочешь научиться танцевать танго (фламенко, ча ча ча)?","326.Хотела бы ты прославиться?","327.Разве можем мы друг без друга?","328.У тебя было когда-нибудь желание уйти в монастырь?","329.Как оценишь по шкале от 1 до 10 свою неадекватность?","330.Оружие в руках хоть раз держала?",
                 "331.На учебу ходила?","332.Чего тебе в жизни не хватает?","333.Ты владеешь языком по-французски?","334.Если я позову на помощь, придешь?","335.Какой у тебя был самый яркий момент в жизни?","336.Ты наверное ходишь в солярий?","337.Ты вроде есть в книге рекордов Гиннеса, как самая красивая девушка. Это правда?","338.Ты где и с кем новый год встречать будешь?","339.Где так загорела, как шоколадка?","340.Давай сделаем это сейчас! Готова?",
                 "341.Как относишься к нудисткому пляжу?","342.Какую песню ты бы выбрала для описания своей жизни?","343.Хочешь выучить какой-нибудь иностранный язык?","344.Ты на каком курсе учишься/будешь учиться?","345.Ты когда-нибудь прыгала/прыгнешь с парашютом?","346.Ты смотришь телевизор?","347.Хочешь поскакать на лошадке?","348.Хочешь я скажу на всех языках мира какая ты красивая?","349.У тебя какой любимый цветок?","350.Ты любишь деньги?",
                 "351.Где находится нофелет?","352.Какое твое любимое блюдо?","353.О чём ты мечтаешь ночью?","354.А я сексуальный?","355.Ты уверенный в себе человек?","356.Ты хоть раз выигрывала в карты на раздевание?","357.Как ты называешь свои интимные места?","358.Ты слышала что ради тебя я бросил бывшую?","359.Если бы я был съедобный, что бы ты съела у меня?","360.Если бы тебе подарили бесплатный билет на самолёт, куда бы ты полетела?",
                 "361.Тебя никто не обижает?","362.Какое твое любимое время года?","363.Отгадай чем ты меня заинтересовала?","364.Ты бы сняла свой секс за деньги?","365.Если кто-то будет писать о тебе книгу, то какое название у нее будет?","366. Ты знала, что в раньше этого вопроса не было и здесь был баг, лол","367.Матом часто ругаешься?","368.Как ты назовешь своих детей?","369.Ты веришь в любовь с первого взгляда?","370.Ты из какой сказки?",
                 "371.Любишь маленьких детей?","372.Фитнесом занимаешься?","373.Я собираюсь снимать фильм про любовь. Хочешь сняться?","374.Во время секса… о чем ты думаешь?","375.Ты вегетарианка?","376.Ты когда-нибудь мучилась от любви?","377.Почему заниматься сексом можно с 16 лет, а курить с 18?","378.Не тебя ли я видел на обложке Playboy?","379.У тебя есть эротическое белье?","380.Если бы тебе осталось жить один час, чтобы ты сделала?",
                 "381.А ты когда-нибудь ходила по городу всю ночь?","382.Дорогая в каком стиле будем наш дом?","383.Ты простишь меня если я тебе случайно изменю?","384.Твое любимое женское и мужское имя?","385.Почему все хотят, чтобы я хотел того, чего хотят они, и никто не хочет хотеть того, чего хочу я?","386.Стакан наполовину пуст или наполовину полон?","387.И каково же чувствовать себя самой прекрасной девушкой в городе?","388.Подскажи, как переводится: «I want you»?","389.Как ты относишься к измене?","390.Кока-кола или Пепси?",
                 "391.Наверное тоже ждешь принца на белом коне?","392.Ты любишь загарать? Топлес?","393.Умеешь рисовать?","394.Ты когда-нибудь ходила на ночной сеанс?","395.Любишь шашлык?","396.Хочешь кушать?","397.Как тебе этот бот, кста?","398. Хочешь услышть вопрос 399?","399.Если честно я не придумал вопрос, так что и так сойде :)))))))))))))","400. Ты знал, что тут всего 400 вопросов?"]

event_aarray=["Делаешь скрин экрана ничего не меняя и кидаешь сюда","Скидываешь последнюю прослушаную песню","Обновляешь сайт www.thiswaifudoesnotexist.net, кидаешь сюда тян которая тебе выпадет и хотел бы ты с ней встречаться","Опиши себя на самоизоляции в 4 мемах","Скидываешь сюда самый смешной мем который ты видел за день"]

t_or_d=["Правда", "Действие"]

owners_id=[2000000012,541720579]

vk = vk_api.VkApi(token="6923f15f9846a22e238106df4e9c227a46bbc8fede3ec9bd16cef4d26121673b1cfca3185114ad13cb1fb")

wikipedia.set_lang("ru")

app = Flask(__name__)
@app.route('/', methods = ["POST"])
def main():
    data = json.loads(request.data)
    if data["type"] == "confirmation":
        return "7d7f3052"
    elif data["type"] == "message_new":
        object = data["object"]
        id = object["peer_id"]
        body = object["text"]

        if id in owners_id:
            if "~сенд" in body.lower():
                ans=list(map(str, (list(map(str, body.lower().split("id:")))[0]).split("~сенд")))[1]
                vk.method("messages.send", {"peer_id":list(map(str, body.lower().split("id:")))[1] , "message":ans, "random_id": random.randint(1, 2147483647)})

        if "~вопросеки" in body.lower():
            if list(map(str, body.lower().split(" ")))[1] == "r":
                count = random.randint(0, 400)
            else:
                count = list(map(str, body.lower().split(" ")))[1]
            vk.method("messages.send", {"peer_id": id, "message":question_aarray[int(count)], "random_id": random.randint(1, 2147483647)})

        if "~ивент" in body.lower():
            vk.method("messages.send", {"peer_id": id, "message":event_aarray[random.randint(0, 3)], "random_id": random.randint(1, 2147483647)})

        if "~кто(ху)" in body.lower():
            if list(map(str, body.lower().split("из ")))[1]== "r":
                anstext=wikipedia.summary(wikipedia.random(pages=1))
            else:
                try:
                    anstext=wikipedia.summary(list(map(str, body.lower().split("из ")))[1],auto_suggest=True)
                except wikipedia.DisambiguationError as e:
                    anstext="Не нашел, попробуйте:\n"
                    for i in range(len(e.options)):
                        anstext+=str(e.options[i])+"\n"
                except wikipedia.exceptions.PageError as e:
                    anstext="Ничего не нашел, соре\n"
            vk.method("messages.send", {"peer_id": id, "message":anstext, "random_id": random.randint(1, 2147483647)})

        if "~алерт" in body.lower():
            n=10
            if "&" in body.lower():
                n=int(list(map(str, body.lower().split("&")))[1])
                for i in range(n):
                    vk.method("messages.send", {"peer_id": id, "message":list(map(str, (list(map(str, body.lower().split("&")))[0]).split("~алерт")))[1], "random_id": random.randint(1, 2147483647)})
            else:
                for i in range(n):
                    vk.method("messages.send", {"peer_id": id, "message":list(map(str, body.lower().split("~алерт")))[1], "random_id": random.randint(1, 2147483647)})

        if "~п/д" in body.lower():
            vk.method("messages.send", {"peer_id": id, "message":t_or_d[random.randint(0, 3)], "random_id": random.randint(1, 2147483647)})

        if "~рандом" in body.lower():
            if "&" in body.lower():
                text123=list(map(str, body.lower().split("~рандом")))[1]
                vk.method("messages.send", {"peer_id": id, "message":random.randint(list(map(int, text123.split("&")))[0],list(map(int, text123.split("&")))[1]), "random_id": random.randint(1, 2147483647)})
            if "|" in body.lower():
                text123=list(map(str, body.lower().split("~рандом")))[1]
                vk.method("messages.send", {"peer_id": id, "message":list(map(str, text123.split("|")))[random.randint(0,len(list(map(str, text123.split("|")))))], "random_id": random.randint(1, 2147483647)})

        if "~хелп" in body.lower():
            ans=list(map(str, body.lower().split("~хелп")))[1]+"\nid:"+str(id)
            for i in range(len(owners_id)):
                vk.method("messages.send", {"peer_id": owners_id[i], "message":ans, "random_id": random.randint(1, 2147483647)})

        if "~стих" in body.lower():
            pages = []
            shit = ""
            shits=""
            pages.append(requests.get('https://yandex.ru/autopoet'))
            for r in pages:
                html = BS(r.content, 'html.parser')
                for i in html.select(".wrapper__content"):
                    text = list(map(str, str(i).split('text":"')))
                    texts = list(map(str, text[1].split('"')))
                    for i in range(len(list(map(str, texts[0].split('n'))))):
                        shit += list(map(str, texts[0].split('n')))[i] + " ."
                    for i in range(len(list(map(str, shit.split('\ .'))))):
                        shits += list(map(str, shit.split('\ .')))[i] + "\n"
            vk.method("messages.send", {"peer_id": id, "message":shits, "random_id": random.randint(1, 2147483647)})

    return "ok"
