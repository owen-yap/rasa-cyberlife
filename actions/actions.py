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
        additional_slots = ["numbness"]
        if tracker.slots.get("numbness"):
            additional_slots.append("numbness_location")
            return additional_slots + slots_mapped_in_domain
        return slots_mapped_in_domain

    def validate_headache_pain_scale(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value.isdecimal() and int(slot_value) <= 10 and int(slot_value) >= 1:
            if int(slot_value) >= 7:
                return {"headache_pain_scale": slot_value, "severe_headache": True}
            else:
                return {"headache_pain_scale": slot_value}
        else:
            dispatcher.utter_message(text = "Sorry, I don't understand that, could you please enter a number from 1 to 10 instead?")
            return {"headache_pain_scale": None}

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

    def extract_numbness_location(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> Dict[Text, Any]:
        if tracker.slots.get("numbness_location") == None:
            return {"numbness_location": tracker.latest_message.get("text")}
        else:
            return {"numbness_location": tracker.slots.get("numbness_location")}

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

class SetRunnyNose(Action):
    def name(self) -> Text:
        return "action_set_runny_nose"

    def run(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("runny_nose", True)]

class SetStuffyNose(Action):
    def name(self) -> Text:
        return "action_set_stuffy_nose"

    def run(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("stuffy_nose", True)]

class SetHeadache(Action):
    def name(self) -> Text:
        return "action_set_headache"

    def run(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        return [SlotSet("headache", True)]

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
