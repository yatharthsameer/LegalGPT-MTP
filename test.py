from rouge_score import rouge_scorer
import bert_score

# Define the RAG and GOLDEN summaries for each case
summaries = {
    "Case 1": {
        "RAG": (
            "The legal document pertains to a bail application filed by Suraj, son of Shri Ladu, under Section 439 of "
            "the Criminal Procedure Code (Cr.P.C.), challenging an order related to FIR No. 67/2016 at Police Station "
            "Nasirabad Sadar, Ajmer, for offenses under Section 8/15 of the NDPS Act. The petitioner argues that the case "
            "against him is false, and his prolonged incarceration since March 8, 2016, without trial conclusion, violates "
            "his right to a speedy trial. The prosecution opposes the bail, citing the recovery of 100 kg of contraband, "
            "exceeding the commercial quantity threshold, thus invoking Section 37 of the NDPS Act. The court acknowledges "
            "the petitioner's long detention and the trial's delay, exacerbated by the recent arrest of an absconded accused, "
            "Mahipal Vishnoi. Citing precedents like Maneka Gandhi v. Union of India and Hussainara Khatoon v. State of Bihar, "
            "the court emphasizes the fundamental right to a speedy trial and the presumption of innocence. The court, "
            "considering the overcrowded prison conditions and the petitioner's lengthy pre-trial detention, grants bail with "
            "conditions, requiring a personal bond and sureties. The decision is influenced by the need to balance the statutory "
            "bar under Section 37 of the NDPS Act with the petitioner's fundamental rights, without affecting the trial's outcome."
        ),
        "GOLDEN": (
            """Observing that despite Supreme Court guidelines, and legal and executive reforms, there is no significant improvement in the state of the under-trials, the Rajasthan High Court recently granted bail to an NDPS accused in view of his over 6 years incarceration as an under-trial.
This Court is anxious over the fact that jails debilitate the under-trial prisoners and if after the long wait, the accused is ultimately acquitted, then how would the long years spent by the under-trial in custody be restored to him/her/them...The issue of a large number of under-trial prisoners and their poor living conditions has been standing stubborn against the otherwise incandescent face of our democracy," the bench of Justice Farjand Ali remarked.
Further, the bench specified the following factors while adjudicating a bail application against the backdrop of the right to a speedy trial:
i) The delay should not have been a defence tactic. Who has caused the delay is also to be seen. Every delay does not necessarily prejudice the accused. 
ii) The aim is not to interpret the right to a speedy trial in a manner so as to disregard the nature of offence, the gravity of punishment, the number of accused and witnesses, prevailing local conditions and other systemic delays. 
iii) If there is a strong reason to believe that the accused will surely flee from justice if released on bail and it will be a hard task for the investigating agency to re-apprehend him, then the benefit of bail should not be extended in his favour. 
iv) If it is shown by placing compelling material on record that the release of the accused may create a ruckus in the society or that he will create such a situation wherein the prosecution witnesses will not come forward to depose against him or that he may otherwise hamper the evidence of prosecution in any other manner, then utmost caution needs to be exercised in such cases before granting bail to the accused.
The bench, however, added that the (iii) and (iv) points are to be considered only when strong and cogent evidence is placed on record or a compelling reason in support has come to light but surely not just on the basis of a simple, blanket submission made by the counsel appearing on behalf of the prosecution/complainant/victim.
The Court further observed that while hearing a bail plea, if there appears the slightest possibility of acquittal of the accused based on any of the submissions made by counsel for the parties, then there is no harm in inclining towards extending the benefit of bail in favor of the accused so far as it is limited to the justifiable disposal of the bail.
"...this Court is of the firm view that the accused should be released on bail if he has been incarcerated pending trial for more than a reasonable period of time unless extraordinary and overwhelming circumstances prevent the Court from doing so...It is the duty of the prosecutor as wells as of the Court to ensure that the prosecution evidence is produced within a reasonable period which must not be an unfair and unjust. In order to justify period of incarceration pending trial, the aid of provision for setting off period of incarceration suffered pending trial with the term of imprisonment decided by the convicting Court in the order of sentence cannot be taken in cases where the trial went on for a long period of time and ultimately resulted into acquittal," remarked the Court.
In a detailed judgment outlining the fundamental right of the accused to a speedy trial and discussing its evolution, the bench referred to an array of Apex Court judgments to observe that an under-trial prisoner cannot be made to wait for the conclusion of the trial for an indefinite period as pre-conviction detention is punitive in nature to a certain extent and goes against the settled principle of criminal jurisprudence that the accused is presumed to be innocent until proven guilty. 
The Court also took into account the pitiable state of the prisons in the Country as it noted that prisoners in India sleep in turns as there is no space for all of them to sleep at the same time. 
"They are packed like sardines in the cells and are deprived of basic needs like balanced diet, sanitation, sewage, hygiene etc. From food and ration to commodities like soap, detergent, toothpaste etc., everything is provided by the state in measured quantities for the number of prisoners that the prison is designated to hold and not for the number of prisoners that it actually holds in reality. In such cases, an under-trial prisoner cannot be subjected to such harsh and inhuman conditions for eons," the Court sternly observed.
Further, the Court also opined that it is high time that the judicial system works on the lacuna of implementation and ensures that a trial is concluded as expeditiously as possible.
The Court also said that the State should maintain a computerized record of all the prisoners and use tools that would indicate the names of the prisoners who have become eligible for release under Section 436A and the names of the prisoners who have otherwise spent a long duration awaiting trial from the database. 
The Court also suggested that there should be a reservoir of police officials as well as legal-aid lawyers in the State to secure the presence of an undertrial prisoner before the lower court timely and to see that no prisoner awaiting trial is made to stay in the prisons longer than necessary.
Significantly, the Court also said that the lawyers should take up such cases pro bono every now and then as so many of the prisoners awaiting trial in the prisons are poor, illiterate, or lacking proper primary and secondary education and are unable to chart out their legal course of action. 
Regarding the case of the petitioner, the Court, while considering the above observations, especially the right to the speedy trial being a fundamental right, the over-crowdedness, and a skewed prison-prisoner ratio, the rightful object of detaining an arrestee and being cognizant of the rigor of Section 37 of the NDPS Act, and in light of the guiding pronouncements of the Apex Court on this issue, though it just and proper to enlarge the petitioner on bail.
Appearances
For Petitioner(s) : Mr. Anil Kumar Upman, Mr. Devanshu Sharma
For Respondent(s) : Mr. Mahendra Meena, PP
Case title - Suraj v. State Of Rajasthan

"""
        ),
    },
    "Case 742": {
        "RAG": (
            "The case involves a petitioner challenging Verification No.09/222 by the Anti-Corruption Bureau (ACB) and seeking "
            "its quashing, alongside an inquiry against respondents 5 to 7 for alleged harassment. The petitioner, a Block Development "
            "Officer, claims that an anonymous complaint led to baseless allegations of corruption and bribery, despite being exonerated "
            "by the Additional Deputy Commissioner, Baramulla. The ACB received multiple complaints against the petitioner, alleging "
            "abuse of position and embezzlement, which are under examination. The petitioner argues that the inquiry is biased, lacks "
            "jurisdiction, and violates protections under the Prevention of Corruption Act, 1988. The High Court, referencing precedents "
            "like State of Telangana v. Habib Abdullah Jeelani and State of Haryana v. Bhajan Lal, emphasized the sparing use of inherent "
            "powers under Section 482 Cr.P.C. to quash proceedings, noting that the case requires a full trial. The petition was dismissed, "
            "with the court finding no grounds to interfere with the ACB's investigation, underscoring the need for a thorough examination "
            "of facts and adherence to legal procedures."
        ),
        "GOLDEN": (
            """The Jammu and Kashmir and Ladakh High Court recently dismissed a petition filed by a woman officer of the J&K Administrative Services (JKAS) seeking to quash the enquiry proceedings initiated against her by the Anti Corruption Bureau, Srinagar in pursuance of an anonymous complaint.
 The petitioner alleged that she was sexually harassed by the SP & Deputy SP of the ACB and was thereafter illegally implicated in a false and frivolous case. She therefore sought directions upon the respondent UT administration to hold an enquiry against the officers concerned.
 She further claimed that she was exonerated by the Additional Deputy Commissioner, however, despite such exoneration she was being harassed by the Investigating Officer and SSP of the ACB for ulterior motives.
 Contesting the plea, the respondents submitted that the Deputy SP, against whom petitioner alleged demand of sexual favours, was not conducting any enquiry in any matter linked with her and that the impugned verification was being conducted as per the Vigilance Manual and procedure applicable in such enquiries. It was claimed that petitioner had concocted a false case with mala fide intent to divert the agency's attention from the probe initiated against her.
 Justice Vinod Chatterji Koul refused to interfere with the investigation in exercise of its powers under Section 482 CrPC, observing:
 "The High Court, while forming an opinion whether a criminal proceeding or complaint or FIR should be quashed in exercise of its jurisdiction under Section 482 Cr. P.C., must evaluate whether the ends of justice would justify the exercise of the inherent power. While inherent power of the High Court has a wide ambit and plenitude, it has to be exercised to secure ends of justice or to prevent an abuse of the process of any Court."
 It added that viewed from all angles, the instant matter demands full dress trial; examination of facts by the High Court in Section 482 jurisdiction as if it is in appeal is not permissible.
 "This is not the aim and objective of provisions of Section 482 Cr. P.C. more particularly when petition on hand does not unveil any ground muchless cogent or material one, to indicate that the inherent powers are to be exercised to prevent abuse of process of law and to secure ends of justice", the bench maintained.
 So far as allegations of sexual harassment are concerned, the High Court recorded in its order that the General Administration Department has officially launched an inquiry against the accused-officers.
 Accordingly, the petition was dismissed.
 Case Title : Dr SI Vs UT of J&K & Ors.
"""
        ),
    },
    "Case 3": {
        "RAG": (
            "The case involves an application under Section 482 Cr.P.C. seeking to quash the charge sheet dated 29.05.2020 and the "
            "proceedings of Criminal Case No. 462 of 2021, arising from case crime no. 251 of 2020. The applicants, including two assistant "
            "teachers, a medical shop owner, and a Hafiz Quran, are accused under various sections of the IPC, Prevention of Cow Slaughter "
            "Act, Prevention of Cruelty to Animals Act, and Environment (Protection) Act. They argue false implication, citing a forensic "
            "report indicating the meat recovered was not cow meat. However, the State contends that 16 live cattle were also found in their "
            "possession without a slaughterhouse license. The court, referencing precedents like R.P. Kapur vs. State of Punjab and State of "
            "Haryana vs. Bhajan Lal, emphasized that quashing is only appropriate when no prima facie case is made out. The court found that "
            "the FIR disclosed a cognizable offense and dismissed the application, noting that the applicants' defense regarding the forensic "
            "report should be addressed during the trial. The decision aligns with the principles laid out in cases like Parbatbhai Aahir and "
            "M/s Neeharika Infrastructure Pvt. Ltd., underscoring that the power under Section 482 Cr.P.C. should be used sparingly and only "
            "in exceptional cases."
        ),
        "GOLDEN": (
            """The Allahabad High Court on Monday refused to quash the criminal case against a government teacher and a madrasa teacher from whose possession cow meat (beef) and 16 live cattle were recovered.
The Bench Justice Rohit Ranjan Agarwal observed that the First Information Report (FIR) that prima facie cognizable offence is made out against the applicants and thus, no case was made out to quash the case against them.
The case in brief
The Court was dealing with the 482 CrPC plea filed by 4 applicants booked under Sections 153- A, 420, 429, 188, 269, 270, 273 I.P.C. and section 3/5/8 of Prevention of Cow Slaughter Act, 1955 and section 11 of Prevention of Cruelty to Animals Act, 1979 and section 7/8 of Environment (Protection) Act, 1986 seeking to quash the case. 
Applicant no. 1 is an Assistant Teacher in the education department of the State, while applicant no. 2 is also working as Assistant Teacher in Madrasa Darul Ulum Gausia Kasba Salempur, while applicant no. 3 is running a medical shop and applicant no. 4 is Hafiz Quran.
It was their submission that a report from the Forensic Investigation Laboratory had received did not disclose that the sample sent for analysis was of the cow. It was their case that no case under the Prevention of Cow Slaughter Act was made out. 
On the other hand, the State counsel argued that the FIR is a detailed report which categorically mentioned that out of 16 live cattle stock which included 7 buffaloes, 1 cow, 2 female buffalo's calf, 5 male buffalo's calf, and one male cow-calf. 
Thus, it was argued by the state that it was wrong to say that the FSL report gave a clean chit to the applicants, as 16 cattle were found in the possession of the applicants and other co-accused and they were not having any license to run the slaughterhouse.
Court's observations 
At the outset, the Court discarded the argument of the applicants that no offence was made out from the reading of the First Information Report, as the Court underscored that even though the FSL report had revealed that the sample which was sent for chemical analysis was not cow meat, but, 16 live cattle were also recovered from the custody of the applicants and another co-accused.
"I find from the perusal of the First Information Report that prima facie cognizable offence is made out against the applicants and only the report of the lab about the chemical analysis of the sample which was sent having been found not to be cow meat but 16 live stock cattle have been found in the custody of the applicants along with other materials, a list of which has been given in First Information Report and there being no license with the applicants for running slaughterhouse, prima facie, the offence is made out and charge sheet having been submitted, and there being serious allegations, no ground is made out for quashing the proceedings..."
Consequently, observing that defence regarding the FSL report shall be considered by the trial court as such defence set up in the present application cannot be considered by this Court at this stage, at the stage of quashing of the charge sheet.
With this, the case was dismissed.
Case title - Parvez Ahmad And 3 Others v. State of U.P. and Another [APPLICATION U/S 482 No. - 17024 of 2022]
"""
        ),
    },
}

# Initialize the ROUGE scorer

# Initialize the ROUGE scorer
scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)

# Calculate ROUGE scores for each case
rouge_scores = {}
for case, texts in summaries.items():
    scores = scorer.score(texts["GOLDEN"], texts["RAG"])
    rouge_scores[case] = scores

# Print ROUGE scores
for case, scores in rouge_scores.items():
    print(f"{case} ROUGE Scores:")
    for metric, score in scores.items():
        print(
            f"  {metric}: Precision: {score.precision:.4f}, Recall: {score.recall:.4f}, F1: {score.fmeasure:.4f}"
        )
    print()

# Now, calculate BERTScore for each case
import bert_score

# Initialize BERTScore
bert_scores = {}
for case, texts in summaries.items():
    P, R, F1 = bert_score.score([texts["RAG"]], [texts["GOLDEN"]], lang="en")
    bert_scores[case] = {
        "Precision": P.mean().item(),
        "Recall": R.mean().item(),
        "F1": F1.mean().item(),
    }

# Print BERTScore results
for case, scores in bert_scores.items():
    print(f"{case} BERTScore:")
    for metric, score in scores.items():
        print(f"  {metric}: {score:.4f}")
    print()
