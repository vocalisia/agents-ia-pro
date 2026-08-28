---
draft: false
domain: "agents-ia.pro"
slug: "mesurer-agent-ia-support-qualite"
title: "Mesurer un agent IA de support : qualité, erreurs et reprise"
description: "Une méthode pour évaluer un agent IA de support sur l’exactitude, les sources, l’abstention, les erreurs et la qualité de la reprise humaine."
date: "2026-08-25"
dateModified: "2026-08-28"
author: "Laurent Duplat"
category: "Support et qualité"
readTime: "15 min de lecture"
image: "/images/article-covers/photo-mesurer-agent-ia-support-qualite.png"
intent: "mesurer la qualité d'un agent IA de support"
persona: "responsable support, qualité ou expérience client"
---

# Mesurer un agent IA de support : qualité, erreurs et reprise

Le nombre de conversations traitées ne mesure pas la qualité d’un agent IA de support. Une réponse peut être rapide et fausse, une conversation peut être clôturée alors que le client n’a pas obtenu de solution, et une escalade peut arriver sans le contexte nécessaire. Pour piloter un agent, mesurez la réponse, la preuve, la limite reconnue et la suite donnée par l’équipe.

Le [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) considère la mesure comme une fonction distincte de la gouvernance et de la gestion. Cette séparation est utile : les responsables décident d’abord ce qui compte, puis observent les cas et corrigent le système. La [CNIL rappelle aussi que l’IA agentique multiplie les sources, la mémoire et les responsabilités](https://www.cnil.fr/fr/ia-agentique-cnil-cianum-note), ce qui rend une mesure limitée à la phrase finale insuffisante.

## Définir la réponse attendue par type de demande

Un support reçoit plusieurs types de demandes. Une question documentaire attend une réponse sourcée. Une demande d’incident attend un diagnostic ou un transfert. Une demande de modification attend une authentification et une action contrôlée. Une demande hors périmètre attend une explication et une orientation.

Pour chaque type, écrivez le comportement attendu. Ne notez pas seulement la formulation. Notez les faits indispensables, la source autorisée, l’action interdite et le moment où l’humain doit reprendre.

Cette étape évite un score trompeur. Un agent peut produire une réponse élégante à une question simple et échouer sur une demande qui exige une vérification. La grille doit refléter le travail réel du support.

## Construire une série de cas

Sélectionnez des cas représentatifs, mais conservez l’origine et la date de chaque cas. Utilisez des données fictives lorsque le test n’est pas encore autorisé sur des demandes réelles. Ajoutez des cas normaux, des formulations différentes, des informations manquantes, des documents contradictoires, des demandes sensibles et des questions sans réponse dans la base.

Pour chaque cas, définissez une sortie acceptable, pas une phrase unique. Une réponse peut être correcte avec deux formulations si elle contient les faits, la source et la limite attendus. Une réponse peut être incorrecte même si elle reprend les bons mots lorsqu’elle invente une condition.

Gardez une série de contrôle hors de la configuration. Rejouez-la après chaque changement important. Sinon, l’équipe mesure sa capacité à ajuster les exemples montrés, pas la robustesse du système.

## Mesurer l’exactitude et la preuve

L’exactitude demande une vérification par une personne qui connaît le processus. La preuve demande de vérifier que la source est la bonne version, que le passage cité répond réellement à la question et que la réponse n’élargit pas la règle.

Utilisez une fiche de cas avec : fait correct, fait absent, fait inventé, source correcte, source ancienne, interprétation excessive, formulation claire et action proposée. La fiche doit pouvoir expliquer l’erreur sans recourir à une note vague.

Une réponse sans source n’est pas toujours fausse. Mais elle doit être classée différemment d’une réponse qui s’appuie sur une documentation identifiée. Cette distinction protège l’équipe quand le support traite des règles susceptibles d’évoluer.

## Mesurer l’abstention

Un agent fiable sait reconnaître une limite. Mesurez les cas où il demande une précision, dit qu’il ne dispose pas de la donnée ou transmet à une personne. Une abstention justifiée peut être une réussite ; une réponse assurée sur une information absente est un échec plus grave.

Créez une taxonomie des abstentions : information manquante, source contradictoire, identité non vérifiée, action non autorisée, problème technique et sujet hors périmètre. Chaque catégorie doit conduire à une suite précise.

Vérifiez aussi les fausses abstentions. Une base mal indexée peut pousser l’agent à transférer une question alors que la réponse existe. Le problème n’est pas alors la consigne de refus, mais la préparation des connaissances ou la recherche.

## Mesurer la reprise humaine

Une reprise réussie permet à la personne de comprendre le dossier sans refaire toute la recherche. Mesurez si le contexte initial, la source consultée, l’incertitude et l’action attendue sont transmis. Demandez à l’utilisateur ce qu’il a dû rechercher à nouveau.

Observez les corrections humaines. Elles peuvent porter sur le fait, la source, la catégorisation, le ton ou l’action. Regroupez ces corrections par cause. Une correction répétée révèle souvent un problème de source, de règle métier ou de permission plutôt qu’un simple problème de formulation.

Mesurez les cas où l’humain valide une réponse sans modification et les cas où il doit la réécrire. Ces observations ne sont pas un verdict universel ; elles servent à décider quel périmètre peut rester assisté.

## Mesurer les outils et les incidents

Ajoutez une trace des appels d’outils : recherche documentaire, lecture d’un dossier, création d’un ticket ou transfert. Vérifiez que l’agent n’annonce pas une action avant confirmation du système. Classez séparément erreur de recherche, erreur d’authentification, délai, doublon et panne.

La [référence OWASP Top 10 pour les applications utilisant des modèles de langage](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/) aide à construire des tests autour de l’injection, de la divulgation et des actions excessives. Ne transformez pas la liste en score marketing. Utilisez chaque risque pour écrire un cas d’essai et une condition d’arrêt.

## Construire un tableau de décision

Un tableau utile contient une ligne par cas et des colonnes qui permettent une décision. Exemple de colonnes : type de demande, source attendue, résultat, preuve, abstention, outil, reprise, correction et décision de périmètre.

Ne combinez pas des critères incompatibles dans une note unique. Une qualité rédactionnelle élevée ne doit pas compenser une divulgation de donnée. Une faible charge de reprise ne doit pas compenser une absence de source. Définissez des critères bloquants, puis observez les critères d’amélioration.

La conclusion peut être : maintenir en assistance, corriger la base, réduire les permissions, réserver à certains cas, suspendre ou retester. Le tableau doit montrer pourquoi.

## Organiser la revue dans le temps

Une mesure n’est valable que pour une configuration, une base documentaire et une période données. Enregistrez la version des consignes, la date de la source, les connecteurs actifs et les changements depuis la précédente revue.

Rejouez une sélection de cas après une mise à jour. Ajoutez les incidents réels sous forme anonymisée et autorisée. Conservez les cas d’échec même après correction : ils servent à vérifier que la régression ne revient pas.

La [CNIL recommande une réflexion sur la finalité, les responsabilités et la minimisation](https://www.cnil.fr/fr/developpement-des-systemes-dia-les-recommandations-de-la-cnil-pour-respecter-le-rgpd). La revue qualité doit donc vérifier aussi les données utilisées pour l’évaluation et le contenu conservé dans les journaux.

## Construire un échantillon qui ressemble au travail

Un échantillon équilibré contient les demandes fréquentes, les formulations courtes, les fautes, les questions incomplètes, les demandes hors périmètre et les cas qui nécessitent un humain. Ne remplacez pas les cas difficiles par des questions faciles pour améliorer un indicateur. L’échantillon doit représenter les situations auxquelles le support devra répondre.

Anonymisez les cas et conservez la version de la source utilisée. Lorsque la réponse attendue dépend d’une règle, demandez à un conseiller de l’écrire avant de regarder la sortie de l’agent. Cette séparation évite de transformer une réponse produite en référence par défaut.

## Distinguer erreur, abstention et transfert

Une abstention est correcte lorsque l’information manque, que la demande sort du périmètre ou qu’une validation est requise. Un transfert est correct lorsque le bon interlocuteur reçoit le contexte. Une erreur apparaît lorsque l’agent répond avec un fait faux, cite une source inadaptée ou promet une action non réalisée.

Classez les incidents selon la conséquence pour l’utilisateur et pour l’équipe. Une réponse un peu longue n’a pas le même poids qu’une instruction incorrecte ou qu’une demande urgente perdue. Le tableau doit conserver le motif afin de guider la correction.

## Mesurer la preuve et la compréhension

Une citation ne suffit pas si elle ne permet pas de retrouver la règle. Vérifiez que le passage cité est pertinent, à jour et lisible par le conseiller. Demandez ensuite à une autre personne de retrouver la décision à partir de la trace. Cette seconde vérification mesure la compréhension réelle.

Observez les corrections. Si les conseillers réécrivent toujours la même phrase, la base ou le gabarit doit être amélioré. Si la correction vient d’un manque de contexte transmis à la reprise, le problème concerne le flux, pas seulement la formulation.

## Construire une boucle de correction

Chaque incident reçoit une suite : corriger la source, ajouter un cas, réduire une permission, modifier une catégorie, améliorer la reprise ou laisser le comportement inchangé avec une explication. La décision est validée par le propriétaire du processus. L’agent ne doit pas apprendre automatiquement d’une correction isolée.

Après une modification, rejouez les cas voisins et un cas réservé. Vérifiez l’amélioration attendue et l’absence de régression sur les demandes sensibles. Archivez l’ancienne mesure pour rendre la comparaison honnête.

## Présenter les résultats à la direction

Commencez par une réponse directe : le périmètre est-il suffisamment fiable pour rester en assistance, doit-il être corrigé, ou doit-il être suspendu ? Ajoutez ensuite les preuves, les limites et la prochaine décision. Évitez une moyenne unique qui masque un échec critique.

Un tableau utile rapproche qualité, abstention, reprise, incidents d’outil et travail de correction. Il indique la période, la version de la base et les permissions actives. La direction peut alors décider sur un système observé, pas sur une impression générale de performance.

## Définir des seuils d’alerte

Un seuil ne doit pas être un chiffre isolé. Reliez-le à une conséquence et à une action. Une hausse des réponses sans source déclenche une revue de contenu. Une hausse des transferts sans contexte déclenche une vérification de la reprise. Une tentative d’action non autorisée déclenche une suspension immédiate selon le périmètre.

Écrivez qui reçoit l’alerte et qui peut décider. Un indicateur ignoré ne protège pas le support. Testez une alerte avec un cas fictif et vérifiez que l’équipe sait retrouver la sortie, la source, la version et la suite.

## Comparer les groupes sans les confondre

Les résultats peuvent varier selon la langue, le canal, le type de demande et le niveau de connaissance. Présentez ces dimensions séparément. Une moyenne globale peut cacher une bonne réponse sur les questions simples et une mauvaise reprise sur les dossiers sensibles.

Ajoutez le volume de cas et les limites de l’échantillon. Une petite série ne permet pas de conclure sur tous les usages. Elle peut néanmoins révéler un incident critique, une source absente ou une permission trop large. La prudence concerne la portée de la conclusion, pas le signalement du problème.

## Mesurer le travail des conseillers

Observez le temps consacré à retrouver la source, corriger le texte, vérifier le statut et reprendre le dossier. Demandez aux conseillers ce qui leur manque pour décider. Une réponse peut être correcte tout en demandant une vérification inutilement longue.

Regroupez les corrections répétées. Elles indiquent une amélioration possible du gabarit, de la base, de l’interface ou de la règle. Ne demandez pas à l’agent de reproduire automatiquement une correction sans validation ; transformez d’abord l’observation en règle claire.

## Rejouer après une modification

Une mise à jour de source, de consigne, de connecteur ou de permission crée une nouvelle version à mesurer. Reprenez les cas de référence, les cas d’incident et quelques variantes. Comparez les sorties et les décisions humaines, puis notez les changements.

Conservez l’ancienne mesure et le motif de la modification. La qualité se juge dans la durée, avec une connaissance et un périmètre identifiés. Un résultat favorable sur une seule journée ne doit pas être présenté comme une propriété permanente de l’agent.

## Rendre la revue actionnable

Chaque revue se termine par une liste courte : maintenir, corriger, réduire, suspendre ou retester. Associez chaque choix à un propriétaire et à un cas qui permettra de vérifier la suite. Cette discipline évite les tableaux qui décrivent un problème sans décider de l’étape suivante.

Présentez aussi ce qui n’a pas été mesuré. Les données personnelles exclues, les canaux non connectés et les actions maintenues en validation humaine doivent apparaître clairement. Une limite déclarée rend la mesure plus crédible qu’une promesse générale.

## La fiche de mesure réutilisable

Conservez la période, le périmètre, la version des consignes, la version des sources, les permissions, la série de cas, la réponse attendue, la sortie, la décision humaine, la preuve, la reprise et l’incident éventuel. Cette fiche permet de comparer deux configurations sans mélanger les causes.

Ajoutez une décision et un propriétaire à chaque constat. Une réponse sans source peut appeler une correction éditoriale ; une action sans validation appelle une réduction de permission ; une reprise sans contexte appelle une amélioration du flux. La mesure devient alors un outil de pilotage.

Ne supprimez pas les échecs une fois corrigés. Ils servent de cas de régression et montrent la limite qui a motivé le changement. La qualité se construit par des boucles visibles, pas par l’effacement des sorties gênantes.

## Relier chaque mesure à une décision

Pour chaque indicateur, écrivez la question à laquelle il répond et la suite prévue. La présence d’une source vérifie la traçabilité ; la correction répétée révèle un problème de connaissance ; l’abstention montre une frontière ; la reprise vérifie la continuité. Sans cette relation, le tableau accumule des nombres sans guider l’équipe.

Demandez à un conseiller de relire la fiche de mesure. Il doit reconnaître les cas, les corrections et les conditions d’arrêt. Si l’indicateur ne correspond pas à une décision qu’il prend réellement, remplacez-le par une observation plus proche du travail.

## Réviser les cas de référence

Gardez des cas normaux et des cas difficiles dans la série de référence. Ajoutez un cas lorsqu’un nouvel incident apparaît, mais conservez les anciens pour vérifier la régression. Documentez les raisons pour lesquelles une réponse est attendue et la source qui permet de la justifier.

Une nouvelle version de la base ou des consignes doit produire une nouvelle mesure. Comparez les cas identiques et expliquez les différences. Cette méthode évite de présenter une amélioration apparente alors que l’échantillon a simplement changé.

La mesure devient utile lorsqu’elle permet de choisir une action et de vérifier son effet. Elle doit donc rester reliée aux cas, aux sources, aux permissions et aux décisions humaines, même lorsque le tableau est présenté à un public non technique.

Terminez chaque revue par un cas à rejouer et une date de vérification. Le tableau reste ainsi lié au travail réel et ne devient pas une photographie sans suite. La qualité se mesure dans la correction et dans la stabilité du parcours, pas seulement dans une première sortie convaincante.

Le compte rendu doit conserver la version des sources et la décision prise, afin que la prochaine mesure soit comparable.

Une mesure sans prochaine vérification décrit un état mais ne pilote pas la qualité. Ajoutez toujours un cas, un propriétaire et une date de reprise.

## Exemple de revue qualité hebdomadaire

La revue choisit des réponses correctes, des abstentions, des transferts et des erreurs. Pour chaque cas, l’équipe relit la demande, la source, la réponse, la décision humaine et le résultat pour l’utilisateur. Elle cherche une cause : source ancienne, catégorie imprécise, permission excessive, incident d’outil ou contexte de reprise incomplet.

La décision qui suit reste courte et attribuée. Une source est corrigée par son propriétaire, une permission est réduite par l’administrateur, un gabarit est revu par l’équipe métier ou un flux est suspendu jusqu’à une recette. Chaque correction ajoute un cas à rejouer.

La semaine suivante, l’équipe compare la nouvelle sortie au cas précédent. Elle ne conclut pas à une amélioration parce que le texte paraît plus fluide : elle vérifie que la source est juste, que l’abstention est appropriée et que le conseiller peut poursuivre sans recherche supplémentaire.

## Vérification de la décision de qualité

À la fin d’une revue, prenez un incident et demandez à une personne de retrouver la source, la version, le motif d’abstention ou l’action de reprise. Si le dossier ne permet pas cette lecture, améliorez le journal ou la fiche de mesure avant de modifier l’agent.

La mesure est réutilisable lorsque chaque correction produit un cas de régression, un propriétaire et une date de contrôle. Elle permet alors de suivre une amélioration sans confondre un nouveau texte plus agréable avec une réponse plus juste ou une reprise plus utile.

## Restitution à l’équipe support

Partagez une synthèse qui montre les réponses utilisées, les abstentions correctes, les reprises difficiles et les corrections décidées. Les conseillers doivent savoir quelle source a changé, quels cas restent humains et comment signaler un nouvel incident. Une mesure restituée ainsi améliore le parcours au lieu de rester un tableau réservé au projet.

La synthèse conserve aussi les limites : canaux non testés, données exclues et actions maintenues en validation. Elle maintient une attente réaliste et donne à l’équipe la prochaine vérification concrète.

## Revoir un échantillon sans confondre rapidité et qualité

Constituez un échantillon qui contient des demandes simples, des demandes incomplètes, des dossiers à deux sujets et des cas qui auraient dû être transmis. Chaque réponse est relue avec la source disponible au moment du traitement, pas avec une procédure corrigée après coup. Le relecteur note séparément la compréhension de la demande, le passage source retrouvé, la formulation remise au client et la décision de continuer ou d’escalader. Cette séparation est essentielle : une réponse polie peut être mal orientée, tandis qu’une abstention peut être la décision la plus sûre pour le conseiller et le client.

Lorsque deux relecteurs ne sont pas d’accord, ne résumez pas leur divergence par une note moyenne. Cherchez l’objet du désaccord. L’un a-t-il interprété une source autrement ? La règle de reprise était-elle absente ? La question initiale comportait-elle une ambiguïté que le formulaire ne permet pas de distinguer ? Le compte rendu doit conserver cet écart et l’action retenue : clarifier une source, préciser un libellé, ajouter un cas de transmission ou retirer une mesure qui ne permet pas une décision. Vous mesurez alors un processus améliorable, pas une impression générale.

Reliez chaque indicateur à une décision précise. Si le nombre de reprises augmente après une mise à jour, l’équipe doit savoir si elle examine la base, la règle de tri ou le canal concerné. Si les réponses paraissent plus rapides mais exigent davantage de correction manuelle, cette observation doit rester visible dans la revue. Une mesure utile indique où regarder ensuite et à qui transmettre le résultat. Elle ne sert pas à déclarer un système satisfaisant à partir d’un seul nombre ou d’un échantillon dont les limites sont oubliées.

Archivez aussi les cas utilisés pour la revue avec leur statut au moment du test. Sans cette trace, une évolution du corpus peut donner l’illusion d’une amélioration alors que le type de demandes a simplement changé.

Avant la revue suivante, tirez au sort une partie des cas et ajoutez-en un issu d’un incident récent, après anonymisation. La sélection reste ainsi proche du travail réel sans se limiter aux dossiers que le projet maîtrise déjà. Indiquez pourquoi chaque cas est présent ; ce contexte permet de lire les résultats sans leur attribuer une portée qu’ils n’ont pas.

## FAQ

### Quel indicateur faut-il regarder en premier ?

Commencez par les erreurs critiques et la qualité de la reprise. Un volume de conversations ou un temps de réponse n’a de sens qu’après avoir vérifié que les demandes sont traitées avec une exactitude et une limite adaptées.

### Une note donnée par l’agent suffit-elle ?

Non. Une auto-évaluation peut signaler un cas incertain, mais elle ne remplace pas la vérification du métier et de la source. Les critères doivent être relus sur les cas.

### Comment éviter de mesurer uniquement les cas faciles ?

Gardez une série de contrôle, ajoutez des cas d’absence et d’ambiguïté, et demandez à des utilisateurs différents de relire les sorties. La diversité des cas est plus informative qu’une longue suite de questions voisines.

## La fiche de mesure à conserver

Conservez la question, le contexte autorisé, la sortie, la source, les appels d’outils, la décision de l’humain, la correction et la configuration. Cette fiche rend l’amélioration reproductible et évite de déclarer une réussite sur la base d’une capture isolée.

Pour préparer la base avant la mesure, lisez [Agent IA support client : préparer les connaissances](/blog/agent-ia-support-preparer-connaissances). Pour organiser un pilote, consultez [Piloter un agent IA en PME](/blog/piloter-pilote-agent-ia-pme). [Contactez Agents-IA.pro](/contact) pour construire une grille adaptée à vos demandes support et à votre reprise humaine.

## Sources de référence

- [NIST — AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [NIST — profil pour l’IA générative](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- [OWASP — Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/)
- [CNIL — IA agentique et données personnelles](https://www.cnil.fr/fr/ia-agentique-cnil-cianum-note)
