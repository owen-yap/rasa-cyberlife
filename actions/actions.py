from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher

class ValidateHistoryTakingForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_history_taking_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        additional_slots = ["confirm_allergy"]
        if tracker.slots.get("confirm_allergy"):
            # If the user has allergies, ask
            # what allergies they have.
            additional_slots.append("allergy")

        return slots_mapped_in_domain + additional_slots

class ValidateCoughForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_cough_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        all_slots = slots_mapped_in_domain
        if tracker.slots.get("cough_type") != "phlegm":
            all_slots.remove("phlegm_color")
        
        return all_slots

    def validate_asthma(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if tracker.get_intent_of_latest_message() == "inform_asthma":
            return{"asthma": slot_value}
        else:
            dispatcher.utter_message(text = "Sorry, I do not quite understand.")
            return{"asthma": None}

    def validate_cough_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:

        if slot_value == "dry":
            return {"dry_cough": True, "cough_type": slot_value}
        elif slot_value == "phlegm":
            return {"cough_with_phlegm": True, "cough_type": slot_value}
        elif slot_value == "blood":
            return {"coughing_up_blood": True, "cough_type": slot_value}
        else:
            return {"cough_type": None}

    def validate_cough_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "more than 3 weeks":
            return {"cough_duration": slot_value, "chronic_cough": True, "persistent_cough": True}
        else:
            return {"cough_duration": slot_value}

    def validate_wheezing(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"wheezing": slot_value, "noisy_breathing": True}
        else:
            return {"wheezing": slot_value}
    
    def validate_shortness_of_breath(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"shortness_of_breath": slot_value, "difficulty_breathing": True}
        else:
            return {"shortness_of_breath": slot_value}

class ValidateFeverForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_fever_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        return slots_mapped_in_domain

    def validate_temperature(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        return {"temperature": slot_value + " °C"}

    def validate_feeling_cold(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"feeling_cold": slot_value, "chills": True}
        else:
            return {"feeling_cold": slot_value}

    def validate_shivering(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"shivering": slot_value, "chills": True}
        else:
            return {"shivering": slot_value}

    def validate_lethargy(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"lethargy": slot_value, "fatigue": True, "weakness": True}
        else:
            return {"lethargy": slot_value}

    def validate_shortness_of_breath(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"shortness_of_breath": slot_value, "difficulty_breathing": True}
        else:
            return {"shortness_of_breath": slot_value}

class ValidateNoseForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_nose_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        return slots_mapped_in_domain

    def validate_stuffy_nose(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"stuffy_nose": slot_value, "nasal_congestion": True}
        else:
            return {"stuffy_nose": slot_value}
    
    def validate_facial_pain(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"facial_pain": slot_value, "sinus_pain": slot_value, "sinus_pressure": slot_value}
        else:
            return {"facial_pain": slot_value}

class ValidateHeadacheForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_headache_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        all_slots = slots_mapped_in_domain
        if tracker.slots.get("numbness") != True:
            all_slots.remove("numbness_location")
        return all_slots

    def validate_headache_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "throbbing":
            return{"headache_type": slot_value, "throbbing_headache": True}
        else:
            return{"headache_type": slot_value}
    
    def validate_headache_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "more than a week":
            return {"headache_duration": slot_value, "persistent_headache": True}
        else:
            return {"headache_duration": slot_value}

    def validate_dizziness(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"dizziness": True, "lightheadedness": True}
        else:
            return {"dizziness": slot_value}

    def validate_numbness_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "hand":
            return {"numbness_location": slot_value, "hand_numbness": True}
        elif slot_value == "leg":
            return {"numbness_location": slot_value, "leg_numbness": True}
        elif slot_value == "foot":
            return {"numbness_location": slot_value, "foot_numbness": True}
        elif slot_value == "others":
            return {"numbness_location": "Enquire further"}
        else:
            dispatcher.utter_message(text = "Sorry, but I could not understand that. Please select either foot, leg, hand or others.")
            return {"numbness_location": None}

    def validate_neck_pain(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"neck_pain": slot_value, "stiff_neck": True}
        else:
            return {"neck_pain": False}

    def validate_facial_pain(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"facial_pain": slot_value, "sinus_pain": slot_value, "sinus_pressure": slot_value}
        else:
            return {"facial_pain": slot_value}

class ValidateEyeForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_eye_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        all_slots = slots_mapped_in_domain
        if tracker.slots.get("photopsia") == False:
            all_slots.remove("photopsia_location")
        
        return all_slots

    def validate_photopsia_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "sides":
            return {"photopsia_location": slot_value}
        elif slot_value == "centre":
            return {"photopsia_location": slot_value}
        else:
            dispatcher.utter_message(text = "Sorry, I do not quite understand")
            return {"photopsia_location": None}

class ValidateAbdominalPainForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_abdominal_pain_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        all_slots = slots_mapped_in_domain
        if tracker.slots.get("abdominal_pain") == False:
            all_slots.remove("abdominal_pain_location")
            all_slots.remove("abdominal_pain_scale")
        if tracker.slots.get("nausea") == False:
            all_slots.remove("vomiting")
        return all_slots

    def validate_stomach_cramps(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"stomach_cramps": slot_value, "cramping": slot_value}
        else:
            return {"stomach_cramps": slot_value}

    def validate_loss_of_appetite(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"loss_of_appetite": slot_value, "poor_appetite": slot_value}
        else:
            return {"loss_of_appetite": slot_value}

    def validate_blood_in_stool(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"blood_in_stool": slot_value, "dark_stool_from_disgested_blood": slot_value}
        else:
            return {"blood_in_stool": slot_value}
        
class SetSymptom(Action):

    def name(self) -> Text:
        return "action_set_symptom"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        symptom = tracker.get_intent_of_latest_message()
        all_slots = tracker.slots
        symptoms = []
        for s in all_slots:
            symptoms.append(s)
        
        if symptom in symptoms:
            if symptom == "dry_cough" or symptom == "cough_with_phlegm" or symptom == "coughing_up_blood":
                return [SlotSet("coughing", True), SlotSet(symptom, True)]
            else:
                return [SlotSet(symptom, True)]
        else:
            return []

class CreateReport(Action):
    def name(self) -> Text:
        return "action_create_report"

    def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        history = ["age", "gender", "allergy", "asthma", "eye_surgery", "diabetes"]
        symptoms_to_present = [
            "coughing",
            "cough_type",
            "phlegm_color",
            "cough_duration",
            "pain_when_coughing",
            "persistent_cough",
            "wheezing",
            "shortness_of_breath",
            "fever",
            "temperature",
            "fever_duration",
            "feeling_cold",
            "shivering",
            "lethargy",
            "stuffy_nose",
            "runny_nose",
            "nasal_congestion",
            "nose_symptom_duration",
            "facial_pain",
            "headache",
            "headache_location",
            "headache_pain_scale",
            "headache_type",
            "headache_duration",
            "head_injury",
            "stress",
            "dizziness",
            "numbness",
            "numbness_location",
            "neck_pain",
            "eye_symptom_location",
            "eye_symptom_duration",
            "eye_redness",
            "eye_pain",
            "eye_pain_scale",
            "eye_injury",
            "eye_discharge",
            "blurred_vision",
            "double_vision",
            "sensitivity_to_light",
            "photopsia",
            "photopsia_location",
            "vision_loss",
            "floaters",
            "contact_lens",
            "abdominal_pain",
            "abdominal_pain_location",
            "abdominal_symptom_duration",
            "abdominal_pain_scale",
            "abdominal_tenderness",
            "abdominal_distension",
            "stomach_cramps",
            "diarrhea",
            "constipation",
            "loss_of_appetite",
            "flank_pain",
            "blood_in_stool",
            "blood_in_urine",
            "dark_urine",
            "pain_during_urination",
            "nausea",
            "vomiting",
            "yellow_skin_and_eyes"
            ]
        all_slots = tracker.slots
        report_slots = {}
        hist = []
        present = []
        absent = []
        for s in all_slots:
            if all_slots[s] == None:
                continue
            elif all_slots[s] == False:
                if s in symptoms_to_present:
                    absent.append(s.replace("_", " "))
            else:
                if s in history and all_slots[s] == True:
                    w = "{}: {}".format(s.replace("_", " "),"Yes")
                    hist.append(w)
                elif s in history and all_slots[s] == False:
                    w = "{}: {}".format(s.replace("_", " "),"No")
                    hist.append(w)
                elif s in history:
                    w = "{}: {}".format(s.replace("_", " "),all_slots[s])
                    hist.append(w)
                else:
                    if s in symptoms_to_present:
                        report_slots[s] = all_slots[s]
        
        for symptom in report_slots:
            if symptom[-8:] == "duration":
                dur = "- Time since onset: " + report_slots[symptom]
                present.append(dur)
            elif symptom[-5:] == "scale":
                scale = "- Intensity: " + report_slots[symptom]
                present.append(scale)
            elif symptom[-8:] == "location":
                loc = "- Location: " + report_slots[symptom]
                present.append(loc)
            elif report_slots[symptom] == True:
                present.append(symptom.replace("_", " "))
            else:
                w = "{}: {}".format(symptom.replace("_", " "),report_slots[symptom])
                present.append(w)

        report = hist + ["Present:\\"] + present + ["Absent:\\"] + absent
        dispatcher.utter_message(text = "\n".join(report))
        return []
