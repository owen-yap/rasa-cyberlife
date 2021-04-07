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
        additional_slots = ["cough_type"]
        if tracker.slots.get("cough_with_phlegm"):
            additional_slots.append("phlegm_color")
        
        return additional_slots + slots_mapped_in_domain

    def validate_asthma(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:

        return{"coughing": True, "asthma": slot_value}

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

    def extract_phlegm_color(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.slots.get("phlegm_color") == None:
            phlegm_color = tracker.latest_message.get("text")
            return {"phlegm_color": phlegm_color}
        else:
            return {"phlegm_color": tracker.slots.get("phlegm_color")}

    def validate_cough_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "more than 8 weeks":
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
        return {"temperature": slot_value + " °C", "fever": True}

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
        additional_slots = []
        if tracker.slots.get("facial_pain"):
            additional_slots.append("sinus_pain_scale")
        return slots_mapped_in_domain + additional_slots

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

class CreateReport(Action):
    def name(self) -> Text:
        return "action_create_report"

    def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        all_slots = tracker.slots
        report_slots = {}
        for s in all_slots:
            if all_slots[s] == False or all_slots[s] == None:
                continue
            else:
                report_slots[s] = all_slots[s]
        for symptom in report_slots:
            if report_slots[symptom] == True:
                report_slots[symptom] = "Yes"
            t = symptom.replace("_", " ") + ": " + report_slots[symptom]
            dispatcher.utter_message(text = t) 
        return []
