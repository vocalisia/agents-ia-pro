---
draft: false
domain: "agents-ia.pro"
slug: "comparer-agents-ia-demo-reelle"
title: "Comparer deux agents IA sans suivre la démo parfaite"
description: "Un protocole pour comparer deux agents IA sur les mêmes entrées, les erreurs, les outils et la reprise humaine, au-delà des démonstrations préparées."
date: "2026-08-25"
dateModified: "2026-08-28"
author: "Laurent Duplat"
category: "Évaluation et comparaison"
readTime: "14 min de lecture"
image: "/images/article-covers/photo-comparer-agents-ia-demo-reelle.png"
intent: "comparatif"
persona: "décideur ou chef de projet IA"
image_brief: "Deux agents IA comparés dans le même banc de test avec cas normal, exception et panne, observateurs humains, illustration technique bleu et orange doux, sans marques"
---

# Comparer deux agents IA sans suivre la démo parfaite

Une démonstration préparée montre ce qu’un agent IA sait faire dans ses meilleures conditions. Une comparaison doit aussi montrer ce qu’il fait lorsqu’une information manque, qu’un outil échoue ou qu’une personne demande une action interdite. Pour comparer deux agents, utilisez les mêmes entrées, sorties attendues et limites.

Le protocole doit être préparé avant de voir les interfaces afin que l’effet visuel ne détermine pas les critères.

## Choisir un parcours complet

Prenez une tâche représentative : qualifier une demande et créer une fiche de test, répondre depuis une base ou préparer un brouillon. Définissez les informations indispensables, l’action finale et la personne qui reprend les exceptions.

Fournissez des données fictives structurées comme les vôtres. N’utilisez pas une consigne optimisée par un seul fournisseur. Laissez chaque équipe configurer son agent, puis testez avec la même formulation utilisateur.

Gardez une variante secrète pour éviter qu’un parcours soit simplement appris pendant la préparation.

## Observer le plan et les appels d’outils

Demandez à voir les étapes ou au moins les journaux d’action. L’agent vérifie-t-il l’identité avant de modifier une fiche ? Confirme-t-il que l’action a réussi avant de l’annoncer ?

Comparez le nombre d’appels seulement dans son contexte. Une séquence courte n’est pas meilleure si elle saute une vérification. Une séquence longue peut augmenter les points de panne sans valeur.

Examinez les permissions. Les deux agents doivent disposer des mêmes droits minimaux afin que l’un ne paraisse plus capable uniquement parce qu’il accède à davantage de données.

## Introduire des erreurs reproductibles

Rendez une source indisponible, fournissez une référence inconnue et placez deux fiches proches. Notez si l’agent s’arrête, demande une précision ou choisit sans preuve.

Ajoutez une consigne adverse dans un document de test. Elle tente de détourner l’objectif ou de demander une action. L’agent doit traiter le contenu comme une donnée non fiable.

Testez la demande d’un humain ou la reprise. Le contexte transmis doit permettre à l’utilisateur de continuer sans recommencer l’enquête.

## Comparer la qualité de la sortie

Créez une grille métier : champs corrects, source visible, catégorie, résumé, action et incertitude. Un texte plus élégant n’est pas meilleur s’il invente un détail ou masque un manque.

Demandez aux futurs utilisateurs de corriger la sortie. Notez ce qu’ils changent et l’effort pour retrouver la source. Leur expérience compte davantage qu’une note générale attribuée par l’équipe projet.

Répétez les scénarios génératifs. Une sortie unique peut être exceptionnellement bonne ou mauvaise.

## Examiner administration et maintenance

Comparez la gestion des utilisateurs, rôles, environnements, versions et journaux. Qui peut modifier les consignes ? Comment une version revient-elle en arrière ? Comment suspendre un outil ?

Demandez comment les sources sont mises à jour et les retours intégrés. Une configuration simple à démontrer peut devenir difficile à maintenir si chaque correction exige le fournisseur.

Regardez aussi la sortie du service : export, suppression, révocation et portabilité des consignes.

## Conclure sans moyenne trompeuse

Définissez des conditions obligatoires : permission minimale, abstention sur un cas, qualité d’un champ ou reprise humaine. Une bonne note sur le style ne doit pas compenser un échec critique.

Le résultat peut varier selon le cas d’usage. Un agent peut être retenu pour la lecture et refusé pour l’action. Documentez cette limite.

## Rejouer la comparaison après configuration

Une première session compare souvent des agents encore mal adaptés. Autorisez chaque fournisseur à corriger les sources, consignes ou correspondances identifiées, puis rejouez exactement les mêmes cas. Notez la nature des changements et le travail nécessaire.

Cette seconde passe mesure la capacité d’amélioration autant que le résultat. Un agent qui devient fiable après une correction simple peut être plus exploitable qu’un outil performant sur la démo mais difficile à ajuster. Gardez toutefois les cas secrets pour vérifier que la correction n’a pas seulement appris les exemples.

## Consulter les rôles de contrôle

Avant la conclusion, faites relire les permissions et le flux de données par les personnes compétentes. Le test fonctionnel ne remplace pas la revue de sécurité, de protection des données ou d’achat. Une option peut gagner sur l’usage tout en exigeant une condition contractuelle ou technique qui retarde son pilote.

Regroupez les conclusions dans une fiche commune et faites valider les désaccords. L’équipe métier et la technique peuvent privilégier des options différentes ; la décision doit expliquer le compromis plutôt que masquer l’écart sous une note moyenne.

## Écrire le banc de test avant les consignes

Un banc de test utile ne se limite pas à une liste de questions. Pour chaque cas, écrivez le contexte disponible, la demande, les éléments que l’agent doit ignorer, la sortie minimale et l’action interdite. Précisez également ce qui constitue un arrêt correct. Cette fiche permet de comparer deux configurations qui n’emploient pas exactement la même interface.

Organisez les cas par famille. La première contient les parcours fréquents et bien documentés. La deuxième introduit une donnée absente ou contradictoire. La troisième vérifie l’identité, les permissions et les doublons. La quatrième simule un incident d’outil. La dernière demande une reprise par un humain. Un agent doit être évalué sur l’ensemble, pas uniquement sur le chemin heureux.

Conservez un identifiant stable pour chaque cas. Lorsque la consigne change, vous pouvez ainsi comparer la nouvelle sortie à l’ancienne sans confondre une amélioration avec un changement de scénario. Gardez quelques cas hors de la préparation des fournisseurs ou de l’équipe qui configure l’outil afin de limiter l’optimisation pour la démonstration.

## Définir une grille de correction

La grille doit distinguer l’exactitude, la complétude et la sécurité. Une réponse peut être exacte mais omettre la condition qui permet de l’appliquer. Elle peut être complète mais exposer une donnée que l’agent ne devait pas utiliser. Elle peut être prudente mais inutile si elle transmet chaque demande sans contexte.

Pour une sortie structurée, vérifiez chaque champ séparément. Notez les champs présents, leur source, leur format et leur niveau de confiance. Pour une réponse documentaire, vérifiez la citation, la date et le périmètre. Pour une action, vérifiez l’autorisation préalable, le résultat dans l’outil et le message donné à l’utilisateur.

Ajoutez une colonne « effort de contrôle ». Elle indique si la personne doit relire une phrase, refaire une recherche ou annuler une action. Cette observation rend visibles les différences que les notes de style ou de vitesse cachent souvent.

## Tester la stabilité, pas une seule réponse

Relancez les cas génératifs avec des formulations naturelles et des détails réordonnés. Le sens doit rester stable. Si une réponse change fortement lorsque la date est placée au début plutôt qu’à la fin, documentez cette sensibilité. Elle peut être acceptable pour une aide exploratoire et inacceptable pour une action écrite dans un système.

Testez aussi le contexte long et les messages successifs. Un agent peut réussir une question isolée puis mélanger deux dossiers lorsque l’échange se prolonge. Vérifiez comment il sépare les utilisateurs, efface une mémoire temporaire et signale une information devenue obsolète.

La répétition ne cherche pas une moyenne flatteuse. Elle sert à repérer les échecs critiques et les conditions qui les déclenchent. Un seul arrêt incorrect sur une opération sensible peut imposer un garde-fou supplémentaire.

## Comparer la reprise humaine

Déclenchez une reprise sur un cas ambigu et observez le paquet transmis. Il doit contenir la demande initiale, les données consultées, les actions déjà tentées, la raison de l’arrêt et la décision attendue. Si l’utilisateur doit recommencer, l’agent a déplacé le travail au lieu de l’assister.

Mesurez le délai de compréhension sans transformer ce nombre en promesse générale. Demandez à plusieurs personnes de reprendre des cas différents et notez les informations qu’elles recherchent. Les écarts indiquent souvent un manque de structure dans le journal ou une règle qui n’est pas expliquée.

Prévoyez une réponse lorsque le service appelé est indisponible. Une bonne reprise indique que l’action n’a pas été confirmée et évite de présenter un résultat supposé comme accompli. Cette distinction est essentielle pour comparer honnêtement deux agents qui n’affichent pas les mêmes détails techniques.

## Décider et conserver la preuve

Le rapport final doit associer chaque conclusion à un cas et à une observation. Remplacez « outil plus intelligent » par « a refusé la fusion sur le cas D‑04 et a transmis le contexte ». Remplacez « intégration simple » par « création d’une tâche observée dans l’environnement de test, avec permission limitée ».

Séparez ce qui est acquis de ce qui reste à vérifier. La décision peut retenir un agent pour une étape et maintenir une validation manuelle pour une autre. Elle peut aussi recommander une nouvelle session après correction des sources. Une comparaison honnête n’a pas besoin d’un vainqueur unique si les usages sont différents.

Archivez les entrées fictives, les versions de consignes, les journaux utiles et la grille remplie. Ne conservez pas de données personnelles dans le dossier de test par facilité. Une future revue doit pouvoir rejouer la logique sans reproduire une exposition inutile.

## Ajouter des cas de frontière

Les cas les plus informatifs se situent entre deux catégories. Écrivez une demande qui ressemble à un cas accepté mais contient une condition d’exclusion. Écrivez une donnée qui peut être interprétée de deux façons. Demandez ensuite à chaque agent d’expliquer ce qui lui manque et de transmettre la question appropriée.

Testez les changements de langue, de format et d’ordre des informations. Une consigne robuste ne devrait pas dépendre d’une phrase parfaitement formulée. Si une traduction perd une condition ou si une pièce jointe est mal comprise, le rapport doit l’indiquer sans extrapoler à tous les usages.

## Tester les droits à plusieurs moments

Les permissions doivent être contrôlées au moment de la lecture et avant l’action. Un droit peut changer pendant une conversation, une tâche peut être réassignée ou une fiche peut devenir sensible. Créez un scénario où le statut se modifie entre deux étapes et vérifiez que l’agent revalide le contexte.

Comparez aussi les journaux accessibles à l’administrateur, au responsable métier et à l’utilisateur. Un agent qui produit une action traçable mais expose toute la conversation à trop de personnes ne passe pas la même évaluation qu’un agent qui sépare correctement les vues.

## Mesurer le travail de préparation

Notez le temps consacré à nettoyer les sources, créer les cas, configurer les connecteurs et corriger les consignes. Ce travail fait partie de la comparaison. Une option peut donner une sortie convaincante après une préparation très lourde, tandis qu’une autre donne une sortie légèrement moins élégante mais plus facile à maintenir.

Ne transformez pas cette observation en classement universel. Le travail de préparation dépend du processus et des compétences disponibles. Il sert à décider si l’équipe peut maintenir le dispositif après la démonstration et qui doit en être responsable.

## Relire les contrats et la documentation opérationnelle

Le test fonctionnel doit être complété par une revue des conditions d’usage, de la suppression, de l’export, des sous-traitants, des journaux et des changements de service. Les points qui concernent votre flux doivent être reliés à une question précise et à une personne chargée de la vérification.

Une fonctionnalité observée dans une session ne répond pas aux questions de gouvernance. Inversement, une documentation favorable ne prouve pas que l’agent produira la bonne sortie sur vos données fictives. Gardez les deux niveaux séparés dans le rapport.

## Formuler une recommandation honnête

La recommandation peut retenir un agent pour lire, un autre pour préparer ou aucun pour écrire. Elle peut proposer un nouveau test, une réduction des permissions ou une amélioration de la base de connaissances. La conclusion doit montrer les limites et les conditions de reprise.

Utilisez une phrase directement exploitable : « poursuivre le pilote sur les demandes entrantes, en lecture et proposition, avec validation humaine pour les dossiers ambigus ». Cette formulation vaut mieux qu’un verdict général qui serait impossible à appliquer.

## Vérifier la documentation de changement

Demandez comment l’équipe est informée d’une évolution du modèle, d’un connecteur ou d’une règle de sécurité. Un changement peut modifier une sortie sans que la consigne locale soit touchée. La comparaison doit prévoir un petit jeu de régression et un propriétaire chargé de le rejouer.

Comparez la qualité annoncée avant et après un changement observé. Notez les cas qui varient et ceux qui restent stables. Cette pratique ne prédit pas le comportement futur, mais elle évite de considérer une session ancienne comme une preuve permanente.

## Examiner les conditions de sortie

Un agent retenu doit pouvoir être suspendu, ses données doivent être récupérables selon le cadre décidé et sa configuration doit être documentée. Testez la révocation d’un connecteur, l’arrêt d’une séquence et le travail manuel de reprise. La comparaison inclut ainsi le jour où l’organisation décide de ne plus utiliser l’outil.

Demandez qui possède les journaux, les sources et les règles métier après la fin du test. Si la réponse n’est pas claire, inscrivez-la comme condition avant la décision. Un résultat fonctionnel ne compense pas une sortie impossible à expliquer.

## Résumer les compromis pour les utilisateurs

Les utilisateurs n’ont pas besoin d’un classement technique complet. Ils ont besoin de savoir ce qui change dans leur geste : proposition à relire, source à vérifier, motif d’arrêt, bouton de reprise et endroit où signaler une erreur. Préparez ce résumé avec eux.

Faites valider le vocabulaire avant la conclusion. Une catégorie qui semble évidente à l’équipe technique peut être incompréhensible au support ou au commerce. Une comparaison réussie produit une décision que les utilisateurs peuvent appliquer et contester.

## La fiche de comparaison finale

Terminez par une fiche qui reprend le scénario, les cas normaux et limites, les droits, les sources, les sorties attendues, les erreurs observées et la reprise. Pour chaque agent, indiquez ce qui a été vu, ce qui a été déclaré et ce qui reste à tester. Cette séparation protège la décision lorsque la démonstration est déjà loin.

Ajoutez les conditions de continuation : périmètre, validation humaine, test de régression et responsable. Ajoutez aussi les conditions d’arrêt : action non autorisée, source non traçable, reprise sans contexte ou impossibilité d’exporter la configuration. Une comparaison utile donne un prochain geste concret.

Ne concluez pas que l’agent gagnant est meilleur dans tous les usages. Dites plutôt pour quel parcours il a satisfait les critères et où ses limites apparaissent. Cette précision réduit la cannibalisation entre décisions et permet de refaire un test lorsque le besoin change.

## Faire signer la fiche de décision

La fiche finale porte le nom du processus, la date, les personnes qui ont observé, les cas exclus et la condition de reprise. Elle évite qu’une comparaison soit réutilisée pour un autre flux sans nouveau test. Un agent retenu pour une lecture documentaire n’est pas automatiquement retenu pour écrire dans un CRM.

Conservez les désaccords importants et la décision qui les résout. Cette trace permet de revenir à une question précise lorsque le périmètre change. Elle protège aussi les utilisateurs contre une conclusion résumée en une phrase trop générale.

Faites une dernière session à l’aveugle : présentez les sorties sans indiquer quel agent les a produites et demandez aux utilisateurs de choisir celle qu’ils pourraient réellement traiter. Comparez ensuite leur choix aux critères de sécurité, de source et de reprise. L’exercice limite l’effet du nom, de l’interface et du discours de démonstration.

Archivez les résultats avec la version des deux configurations. La comparaison ne doit pas être réutilisée comme une vérité intemporelle ; elle décrit un parcours, une période et des droits déterminés.

Ajoutez la date de la prochaine comparaison et le déclencheur qui l’imposera : changement de source, permission, modèle, connecteur ou processus. Cette dernière étape transforme le comparatif en outil de gouvernance et empêche une ancienne démo de rester la référence par défaut.

Le rapport doit rester lisible par les utilisateurs : cas, résultat, limite et suite. Cette forme évite de confondre une capacité observée avec une promesse valable pour tous les parcours.

Conservez au moins un cas non montré pendant la démonstration. Il vérifie que la configuration répond à la logique du processus et pas seulement aux exemples préparés. La conclusion doit indiquer si ce cas a réussi, demandé une précision ou déclenché une reprise.

## Exemple de fiche de résultat

Pour un cas de demande support, la fiche peut dire : « Agent A retrouve la procédure et cite le bon passage, mais transmet un fil incomplet lorsque deux sujets sont présents. Agent B s’arrête plus souvent, mais transmet le message, la source consultée et la question à traiter. » Cette formulation n’attribue pas une qualité abstraite : elle relie une observation à un geste utilisateur.

Ajoutez la conséquence métier. Si le conseiller doit traiter un fil complexe, le contexte transmis peut compter davantage qu’une réponse automatique plus fréquente. Si la tâche est une simple recherche documentaire, la capacité à citer une source à jour peut devenir le critère prioritaire.

La fiche conclut par une action : poursuivre le test sur un périmètre défini, demander une correction de reprise, ou maintenir les deux options en observation. Elle évite le faux choix d’un « gagnant » lorsque les agents répondent à des étapes différentes.

## Mettre les démonstrations sous contradiction

Une comparaison devient utile lorsque les mêmes cas peuvent démentir une impression favorable. Constituez un petit jury avec une personne métier, une personne chargée de la conformité du processus et une personne qui devra administrer le flux. Chacune reçoit les mêmes dossiers de recette, dans le même ordre, sans voir la réponse de l’autre. Leur rôle n’est pas de noter un ton ou une vitesse apparente ; elles vérifient ce qui a été lu, ce qui est proposé, ce qui est transmis et ce qui reste impossible à justifier.

Prévoyez au moins un cas qui contredit une information déjà présente. Une demande peut citer un ancien contact, une procédure peut avoir changé, ou deux sources peuvent orienter vers des actions différentes. L’agent qui signale cette contradiction et prépare une reprise claire mérite une observation plus utile que celui qui choisit silencieusement une version. Inscrivez donc dans la fiche le comportement attendu en cas de conflit, puis comparez l’écart exact : source manquante, contexte perdu, action trop large ou arrêt correctement déclenché.

À la fin de la séance, le jury rédige une décision formulée comme une limite de travail : « utilisable pour préparer telle étape sous telle validation » ou « à écarter tant que telle trace manque ». Évitez les classements absolus. Un outil peut aider à retrouver une procédure sans être prêt à qualifier une demande, et un autre peut être pertinent sur le tri tout en restant fragile sur la reprise. Cette conclusion préserve l’intention de la comparaison : choisir un comportement adapté à une tâche donnée, pas établir une vérité générale sur les agents examinés.

## Questions fréquentes

### Peut-on comparer à partir de vidéos ?

Elles aident à découvrir, mais ne permettent pas d’imposer les mêmes entrées ni de tester les erreurs. Une session interactive est nécessaire.

### Faut-il utiliser les données de l’entreprise ?

Pas au début. Des données fictives peuvent reproduire les formats et exceptions. Les données réelles attendent la validation du cadre.

### Quel utilisateur inviter ?

Une personne qui réalise la tâche et sait reconnaître une erreur. Le sponsor seul ne voit pas toujours les détails de sortie.

## Organiser une comparaison

[Contactez Agents-IA.pro](/contact) pour construire un banc de test commun et comparer des agents sur vos critères métier.

## À lire ensuite

Pour compléter cette étape, consultez [Agent IA support client : préparer les connaissances](/blog/agent-ia-support-preparer-connaissances).

Pour vérifier le point suivant, poursuivez avec [Choisir un agent IA adapté au métier de votre PME](/blog/choisir-agent-ia-metier-pme).

Pour replacer cette décision dans l’ensemble du dossier, lisez [Déployer un agent IA commercial avec garde-fous](/blog/deployer-agent-ia-commercial-garde-fous).

Pour éviter une analyse isolée, rapprochez ce guide de [Marketplace d’agents IA : critères de sélection utiles](/blog/marketplace-agents-ia-criteres-selection).

## Sources de référence

Ces références permettent de vérifier les règles, les méthodes et les limites évoquées dans l’article.

Pour contrôler les éléments factuels, consultez [EUR-Lex — règlement européen sur l’IA](https://eur-lex.europa.eu/eli/reg/2024/1689/oj) : Cadre officiel européen pour les obligations, les risques et la gouvernance des systèmes d’IA.

Pour contrôler les éléments factuels, consultez [NIST — AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) : Cadre public de référence pour gouverner, mesurer et maîtriser les risques liés à l’IA.

Pour contrôler les éléments factuels, consultez [CNIL — intelligence artificielle](https://www.cnil.fr/fr/intelligence-artificielle) : Recommandations françaises sur l’IA, les données personnelles et les droits des personnes.
