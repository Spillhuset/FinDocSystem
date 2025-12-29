# Finance documentation

Bot for handling and creating documentation.
Norsk: En bot for å behandle og generere dokumentasjon.

---
## The idea:
1. User presses "new receipt".


## Bilag for utleggsoppgjør
Bruker trykker på [Nytt utlegg]


- Navn og Telefonnummer
- Formål med billaget
- Dato (settes automatisk)
- Kontonummer
- Ønskes refundert innen dato

Liste over vedlegg. (et vedlegg per rad) 

Bruker for popup til å laste opp bilder: {File Upload}
- Dersom brukeren laster opp flere bilder, blir de slått sammen til en pdf.


*Bruker laster opp bildet/pdf*

Får følgende felt 
- Hvor regningen er fra (regning fra) {Tekst felt}
- Hva det gjelder (Gjelder) {Tekst felt}
- Dato for kjøp {Dato felt}
- sum kr.

Får da en meny med:

[Send til godkjenning] [Last opp flere vedlegg] [Forkast vedlegg]

Om den sendes til godkjenning fryses [Last opp flere vedlegg]

Vedleggets navn blir lagret.
Sum utgifter blir kallkulert.