from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
import infermedica_api
import numpy as np
import pandas as pd

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
        slot_order = [
            "abdominal_pain",
            "abdominal_pain_type",
            "abdominal_pain_location",
            "abdominal_pain_duration",
            "abdominal_pain_onset",
            "abdominal_pain_scale",
            "abdominal_tenderness",
            "abdominal_tenderness_location",
            "abdominal_pain_postprandial",
            "abdominal_pain_premenstrual",
            "abdominal_pain_exacerbation",
            "bloating",
            "abdominal_mass",
            "fever",
            "temperature",
            "diarrhea",
            "diarrhea_duration",
            "constipation",
            "nausea",
            "vomiting",
            "vomiting_duration",
            "vomiting_every_time_after_meal",
            "vomiting_more_often_in_the_morning",
            "diminished_appetite",
            "stools",
            "painful_defecation",
            "bleeding_from_anus",
            "bleeding_from_anus_scale",
            "blood_in_urine",
            "pain_while_urinating"
        ]
        if tracker.slots.get("abdominal_pain") == False:
            slot_order.remove("abdominal_pain_type")
            slot_order.remove("abdominal_pain_location")
            slot_order.remove("abdominal_pain_duration")
            slot_order.remove("abdominal_pain_onset")
            slot_order.remove("abdominal_pain_scale")
            slot_order.remove("abdominal_tenderness")
            slot_order.remove("abdominal_tenderness_location")
            slot_order.remove("abdominal_pain_postprandial")
            slot_order.remove("abdominal_pain_premenstrual")
        if tracker.slots.get("abdominal_tenderness") == False:
            slot_order.remove("abdominal_tenderness_location")
        if tracker.slots.get("gender") == "male":
            if "abdominal_pain_premenstrual" in slot_order:
                slot_order.remove("abdominal_pain_premenstrual")
        if tracker.slots.get("fever") == False:
            slot_order.remove("temperature")
        if tracker.slots.get("diarrhea") == False:
            slot_order.remove("diarrhea_duration")
        if tracker.slots.get("vomiting") == False:
            slot_order.remove("vomiting_duration")
            slot_order.remove("vomiting_every_time_after_meal")
            slot_order.remove("vomiting_more_often_in_the_morning")
        if tracker.slots.get("stools") == "Normal":
            slot_order.remove("painful_defecation")
            slot_order.remove("bleeding_from_anus")
            slot_order.remove("bleeding_from_anus_scale")
        return slot_order

    def validate_abdominal_pain_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "cramping":
            return {"abdominal_pain_crampy": True, "abdominal_pain_type": slot_value}
        elif slot_value == "burning or gnawing":
            return {"abdominal_pain_burning_or_gnawing": True, "abdominal_pain_type": slot_value}
        elif slot_value == "sharp and stabbing":
            return {"abdominal_pain_sharp_and_stabbing": True, "abdominal_pain_type": slot_value}
        elif slot_value == "others":
            return {"abdominal_pain_type": "Unknown"}
        else:
            dispatcher.utter_message(text = "I do not quite understand, maybe try selecting one of the options?")
            return  {"abdominal_pain_type": None}

    def validate_abdominal_pain_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:            
        if slot_value == "left upper":
            return {"abdominal_pain_left_side": True, "abdominal_pain_left_upper_quadrant": True, "abdominal_pain_localised": True, "abdominal_pain_location": slot_value}
        elif slot_value == "left lower":
            return {"abdominal_pain_left_side": True, "abdominal_pain_left_lower_quadrant": True, "abdominal_pain_localised": True, "abdominal_pain_location": slot_value}
        elif slot_value == "right upper":
            return {"abdominal_pain_right_side": True, "abdominal_pain_right_upper_quadrant": True, "abdominal_pain_localised": True, "abdominal_pain_location": slot_value}
        elif slot_value == "right lower":
            return {"abdominal_pain_right_side": True, "abdominal_pain_right_lower_quadrant": True, "abdominal_pain_localised": True, "abdominal_pain_location": slot_value}
        elif slot_value == "centre":
            return {"abdominal_pain_periumbilical": True, "abdominal_pain_localised": True, "abdominal_pain_location": slot_value}
        elif slot_value == "flanks":
            return {"flank_pain": True, "abdominal_pain_localised": True, "abdominal_pain_location": slot_value}
        elif slot_value == "pelvis":
            return {"abdominal_pain_pelvic": True, "abdominal_pain_localised": True, "abdominal_pain_location": slot_value}
        elif slot_value == "all over":
            return {"abdominal_pain_diffuse": True, "abdominal_pain_location": slot_value}
        else:
            dispatcher.utter_message(text = "Please select one of the options")
            return {"abdominal_pain_location": None}

    def validate_abdominal_pain_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:            
        if slot_value == "less than 2 days":
            return {"abdominal_pain_lasting_less_than_two_days": True, "abdominal_pain_duration": slot_value}
        elif slot_value == "between 2 to 7 days":
            return {"abdominal_pain_lasting_2_to_7_days": True, "abdominal_pain_duration": slot_value}
        elif slot_value == "between 1 to 2 weeks":
            return {"abdominal_pain_lasting_8_to_14_days": True, "abdominal_pain_duration": slot_value}
        elif slot_value == "more than 2 weeks":
            return {"abdominal_pain_lasting_more_than_two_weeks": True, "abdominal_pain_duration": slot_value}
        else:
            dispatcher.utter_message(text = "Please select one of the options")
            return {"abdominal_pain_duration": None}

    def validate_abdominal_pain_onset(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "gradual":
            return {"abdominal_pain_gradual_onset": True, "abdominal_pain_onset": slot_value}
        elif slot_value == "sudden":
            return {"abdominal_pain_sudden_onset": True, "abdominal_pain_onset": slot_value}
        else:
            dispatcher.utter_message(text = "Please select one of the options")
            return {"abdominal_pain_onset": None}

    def validate_abdominal_pain_scale(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "mild":
            return {"abdominal_pain_mild": True, "abdominal_pain_scale": slot_value}
        elif slot_value == "moderate":
            return {"abdominal_pain_moderate": True, "abdominal_pain_scale": slot_value}
        elif slot_value == "severe":
            return {"abdominal_pain_severe": True, "abdominal_pain_scale": slot_value}
        else:
            dispatcher.utter_message(text = "Please select one of the options")
            return {"abdominal_pain_onset": None}

    def validate_abdominal_tenderness_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "left upper":
            return {"abdominal_tenderness_left_upper_quadrant": True, "abdominal_tenderness_location": slot_value}
        elif slot_value == "left lower":
            return {"abdominal_tenderness_left_lower_quadrant": True, "abdominal_tenderness_location": slot_value}
        elif slot_value == "right upper":
            return {"abdominal_tenderness_right_upper_quadrant": True, "abdominal_tenderness_location": slot_value}
        elif slot_value == "right lower":
            return {"abdominal_tenderness_right_lower_quadrant": True, "abdominal_tenderness_location": slot_value}
        elif slot_value == "pelvis":
            return {"abdominal_tenderness_suprapubic": True, "abdominal_tenderness_location": slot_value}
        else:
            dispatcher.utter_message(text = "Please select one of the options")
            return {"abdominal_tenderness_location": None}

    def validate_abdominal_pain_exacerbation(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "after caffeine consumption":
            return {"abdominal_pain_exacerbating_after_caffeine_consumption": True, "abdominal_pain_exacerbation": slot_value}
        elif slot_value == "during coughing or movement":
            return {"abdominal_pain_exacerbating_during_coughing_or_movement": True, "abdominal_pain_exacerbation": slot_value}
        elif slot_value == "during deep breaths":
            return {"abdominal_pain_exacerbating_during_deep_breath": True, "abdominal_pain_exacerbation": slot_value}
        elif slot_value == "on an empty stomach":
            return {"abdominal_pain_exacerbating_on_an_empty_stomach": True, "abdominal_pain_exacerbation": slot_value}
        elif slot_value == "when under stressed":
            return {"gastrointestinal_complaints_stress_related": True, "abdominal_pain_exacerbation": slot_value}
        elif slot_value == "no":
            return {"abdominal_pain_exacerbation": "None"}
        else:
            dispatcher.utter_message(text = "Please select one of the following options")
            return {"abdominal_pain_exacerbation": None}

    def validate_diarrhea_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "less than 2 days":
            return {"diarrhea_lasting_less_than_48_hours": True, "diarrhea_duration": slot_value}
        elif slot_value == "between 2 days and 2 weeks":
            return {"diarrhea_lasting_2_to_14_days": True, "diarrhea_duration": slot_value}
        elif slot_value == "more than 2 weeks":
            return {"diarrhea_lasting_more_than_14_days": True, "diarrhea_duration": slot_value}
        else:
            dispatcher.utter_message(text = "Please select one of the following options")
            return {"abdominal_pain_exacerbation": None}

    def validate_vomiting_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "less than a week":
            return {"vomiting_less_than_7_days": True, "vomiting_duration": slot_value}
        elif slot_value == "more than a week":
            return {"vomiting_7_days_or_more": True, "vomiting_duration": slot_value}
        else:
            dispatcher.utter_message(text = "Please select one of the following options")
            return {"vomiting_duration": None}


    def validate_stools(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "black feces":
            return {"black_stools": True, "stools": slot_value}
        elif slot_value == "blood in feces":
            return {"blood_in_stool": True, "stools": slot_value}
        elif slot_value == "no":
            return {"stools": "Normal"}
        else:
            dispatcher.utter_message(text = "Please select one of the following options")
            return {"vomiting_duration": None}
            
    def validate_bleeding_from_anus_scale(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "light":
            return {"bleeding_from_anus_light": True, "bleeding_from_anus_scale": slot_value}
        elif slot_value == "heavy":
            return {"bleeding_from_anus_heavy": True, "bleeding_from_anus_scale": slot_value}
        else:
            dispatcher.utter_message(text = "Please select one of the following options")
            return {"vomiting_duration": None}
            
class ValidateUrtiForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_urti_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        all_slots = slots_mapped_in_domain
        if tracker.slots.get("fever") == False:
            all_slots.remove("temperature")
        if tracker.slots.get("cough") == False:
            all_slots.remove("cough_duration")
            all_slots.remove("cough_productive")
            all_slots.remove("hemoptysis")
            all_slots.remove("cough_productive_color")
            all_slots.remove("cough_nocturnal")
            all_slots.remove("cough_paroxysmal")
        if tracker.slots.get("cough_productive") == False:
            all_slots.remove("cough_productive_color")
        if tracker.slots.get("nasal_congestion") == False:
            all_slots.remove("nasal_congestion_chronic")
        if tracker.slots.get("facial_pain") == False:
            all_slots.remove("facial_pain_paranasal_sinus")
            all_slots.remove("facial_pain_longer_than_a_couple_of_hours")
        if tracker.slots.get("dyspnea") == False:
            all_slots.remove("dyspnea_severity")
            all_slots.remove("dyspnea_duration")
            all_slots.remove("dyspnea_orthopnea")
        if tracker.slots.get("chest_pain") == False:
            all_slots.remove("chest_pain_type")
            all_slots.remove("chest_pain_duration")
            all_slots.remove("chest_pain_exacerbated_by_stress")
            all_slots.remove("chest_pain_during_exertion")
            all_slots.remove("chest_pain_exacerbating_with_deep_breath_or_cough")
            all_slots.remove("chest_pain_exacerbating_when_lying_down")
            all_slots.remove("chest_pain_radiating")
        return all_slots
        
    def validate_temperature(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:

        def check_float(potential_float):
            try:
                float(potential_float)
                return True
            except ValueError:
                return False
        
        if slot_value.isnumeric() or check_float(slot_value):
            temp = float(slot_value)
            if temp <= 38 and temp >=37:
                return {"temperature": slot_value, "fever_between_37_and_38": True}
            elif temp > 38 and temp <= 40:
                return {"temperature": slot_value, "fever_between_38_and_40": True}
            elif temp > 40:
                return {"temperature": slot_value, "fever_greater_than_40": True}
            else:
                return {"temperature": slot_value}
        else:   
            dispatcher.utter_message(text = "Please enter in a number")
            return {"temperature": None}

    def validate_cough_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "less than 3 weeks":
            return {"cough_duration": slot_value, "cough_lasting_less_than_three_weeks": True}
        elif slot_value == "3 to 8 weeks":
            return {"cough_duration": slot_value, "cough_lasting_three_to_eight_weeks": True}
        elif slot_value == "more than 8 weeks":
            return {"cough_duration": slot_value, "cough_lasting_more_than_eight_weeks": True}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"cough_duration": None}

    def validate_cough_productive(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"cough_productive": slot_value, "cough_dry": False}
        elif slot_value == False:
            return {"cough_productive": slot_value, "cough_dry": True}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"cough_productive": None}

    def validate_cough_productive_color(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "pink and frothy":
            return {"cough_productive_color": slot_value, "cough_productive_with_pink_frothy_sputum": True}
        elif slot_value == "yellow or green":
            return {"cough_productive_color": slot_value, "cough_productive_with_yellow_or_green_sputum": True}
        elif slot_value == "others":
            return {"cough_productive_color": "unknown"}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"cough_productive_color": None}

    def validate_nasal(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "runny nose":
            return {"nasal": slot_value, "nasal_catarrh": True}
        elif slot_value == "blocked nose":
            return {"nasal": slot_value, "nasal_catarrh": True, "nasal_congestion": True}
        elif slot_value == "both":
            return {"nasal": "Runny and blocked nose", "nasal_catarrh": True, "nasal_congestion": True}
        elif slot_value == "no":
            return {"nasal": "No runny or blocked nose", "nasal_congestion": False}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"nasal": None}
            
    def validate_dyspnea_severity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "when resting":
            return {"dyspnea_at_rest": True}
        elif slot_value == "after few minutes of walking":
            return {"dyspnea_after_a_few_minutes_of_walking": True}
        elif slot_value == "when i do physical activities":
            return {"dyspnea_on_exertion": True}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"dyspnea_severity": None}

    def validate_dyspnea_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "less than 1 hour":
            return {"dyspnea_lasting_less_than_1_hour": True}
        elif slot_value == "1 to 24 hours":
            return {"dyspnea_lasting_1_to_24_hours": True}
        elif slot_value == "1 day to 4 weeks":
            return {"dyspnea_lasting_1_day_to_4_weeks": True}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"dyspnea_duration": None}

    def validate_chest_pain_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "burning":
            return {"chest_pain_type": slot_value, "chest_pain_burning": True}
        elif slot_value == "pressing":
            return {"chest_pain_type": slot_value, "chest_pain_pressure": True}
        elif slot_value == "stabbing":
            return {"chest_pain_type": slot_value, "chest_pain_stabbing": True}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"chest_pain_type": None}

    def validate_chest_pain_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "less than 30 minutes":
            return {"chest_pain_duration": slot_value, "chest_pain_lasting_less_than_30_minutes": True}
        elif slot_value == "between 30 minutes and 8 hours":
            return {"chest_pain_duration": slot_value, "chest_pain_lasting_between_30_minutes_and_8_hours": True}
        elif slot_value == "more than 8 hours":
            return {"chest_pain_duration": slot_value, "chest_pain_lasting_over_8_hours": True}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"chest_pain_duration": None}

    def validate_chest_pain_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "spreading to left upper limb":
            return {"chest_pain_location": slot_value, "chest_pain_radiating_to_left_upper_limb": True}
        elif slot_value == "spreading to neck":
            return {"chest_pain_location": slot_value, "chest_pain_radiating_to_the_neck": True}
        elif slot_value == "spreading to shoulders":
            return {"chest_pain_location": slot_value, "chest_pain_radiating_between_shoulder_blades": True}
        elif slot_value == "not spreading":
            return {"chest_pain_location": slot_value}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"chest_pain_location": None}

class ValidateBackPainForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_back_pain_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        all_slots = slots_mapped_in_domain
        if tracker.slots.get("back_pain_lumbar") == False:
            all_slots.remove("back_pain_lumbar_radiates_to_back_of_the_thigh")
            all_slots.remove("back_pain_lumbar_radiating_to_the_groin")

    def validate_back_pain_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "upper back":
            return {"back_pain_location": slot_value, "back_pain_thoracic": True, "back_pain_lumbar": False}
        elif slot_value == "lower back":
            return {"back_pain_location": slot_value, "back_pain_lumbar": True}
        elif slot_value == "both upper and lower back":
            return {"back_pain_location": "upper and lower back", "back_pain_lumbar": True, "back_pain_thoracic": True}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"back_pain_location": None}

    def validate_back_pain_scale(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "mild":
            return {"back_pain_scale": slot_value}
        elif slot_value == "moderate":
            return {"back_pain_scale": slot_value}
        elif slot_value == "severe":
            return {"back_pain_scale": slot_value, "back_pain_severe": True}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"back_pain_scale": None}

class ValidateBreastPainForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_breast_pain_form"

    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        return slots_mapped_in_domain

    def validate_breast_pain(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "only one breast":
            return {"breast_pain": slot_value, "breast_pain_or_tenderness_unilateral": True}
        elif slot_value == "both breasts":
            return {"breast_pain": slot_value, "breast_pain_or_tenderness_bilateral": True}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"back_pain_scale": None}

    def validate_abnormal_breast_size(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "larger than normal":
            return {"abnormal_breast_size": slot_value, "enlarged_breasts": True}
        elif slot_value == "smaller than normal":
            return {"abnormal_breast_size": slot_value, "decreased_breast_size": True}
        elif slot_value == "no change in size":
            return {"abnormal_breast_size": slot_value, }
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"back_pain_scale": None}

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
        if tracker.slots.get("headache_chronic") == True:
            all_slots.remove("headache_recent")
            all_slots.remove("headache_recent_lasting_for_more_than_1_hour_and_less_than_1_day")
            all_slots.remove("headache_recent_lasting_less_than_1_hour")
            all_slots.remove("headache_recent_lasting_more_than_1_day")
            all_slots.remove("headache_recent_duration")
        if tracker.slots.get("headache_chronic") == False:
            all_slots.remove("headache_chronic")
            all_slots.remove("headache_chronic_attack_lasting_4_to_72_hours")
            all_slots.remove("headache_chronic_attack_lasting_five_minutes_to_four_hours")
            all_slots.remove("headache_chronic_attack_lasting_three_to_seven_days")
            all_slots.remove("headache_chronic_attack_lasting_up_to_five_minutes")
            all_slots.remove("headache_duration")
        if tracker.slots.get("neck_pain") == False:
            all_slots.remove("neck_pain_during_head_movement")
            all_slots.remove("neck_pain_unilateral")
        if tracker.slots.get("impaired_memory") == False:
            all_slots.remove("impaired_memory_finding_objects_of_everyday_use")
            all_slots.remove("impaired_memory_short_term")      
        if tracker.slots.get("dizziness") == False:
            all_slots.remove("dizziness_head_rotation")
            all_slots.remove("dizziness_vertigo")       
            all_slots.remove("orthostatic_hypotension")
        if tracker.slots.get("tremors") == False:
            all_slots.remove("tremors_worsen")
            all_slots.remove("tremors_hands")
            all_slots.remove("tremors_both_hands")
            all_slots.remove("tremors_in_one_hand")       
            all_slots.remove("tremors_stress_related")
            all_slots.remove("tremors_subside_after_drinking_alcohol")       
            all_slots.remove("tremors_worsen_after_caffeine_intake")
        if tracker.slots.get("headache_lancinating") == True:
            all_slots.remove("headache_pressing")
            all_slots.remove("headache_pulsating")  
        if tracker.slots.get("headache_pressing") == True:
            all_slots.remove("headache_lancinating")
            all_slots.remove("headache_pulsating")    
        if tracker.slots.get("headache_pulsating") == True:
            all_slots.remove("headache_pressing")
            all_slots.remove("headache_lancinating")        
        if tracker.slots.get("tremors_stress_related") == True:
            all_slots.remove("tremors_subside_after_drinking_alcohol")
            all_slots.remove("tremors_worsen_after_caffeine_intake")  
        if tracker.slots.get("tremors_subside_after_drinking_alcohol") == True:
            all_slots.remove("tremors_stress_related")
            all_slots.remove("tremors_worsen_after_caffeine_intake")    
        if tracker.slots.get("tremors_worsen_after_caffeine_intake") == True:
            all_slots.remove("tremors_subside_after_drinking_alcohol")
            all_slots.remove("tremors_stress_related")      
        if tracker.slots.get("headache_mild") == True:
            all_slots.remove("headache_moderate")
            all_slots.remove("headache_severe")  
        if tracker.slots.get("headache_moderate") == True:
            all_slots.remove("headache_mild")
            all_slots.remove("headache_severe")    
        if tracker.slots.get("headache_severe") == True:
            all_slots.remove("headache_mild")
            all_slots.remove("headache_moderate")  
    
        if tracker.slots.get("headache_generalized") == True:
            all_slots.remove("headache_unilateral")


        return all_slots


    def validate_headache_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Chronic, attack lasting 4 to 72 hours":
            return{"headache_duration":slot_value,"headache_chronic_attack_lasting_4_to_72_hours": True,"headache_chronic_attack_lasting_five_minutes_to_four_hours": False,"headache_chronic_attack_lasting_three_to_seven_days": False,"headache_chronic_attack_lasting_up_to_five_minutes": False  }
        elif slot_value == "Chronic, attack lasting five minutes to four hours":
            return{"headache_duration":slot_value,"headache_chronic_attack_lasting_4_to_72_hours": False,"headache_chronic_attack_lasting_five_minutes_to_four_hours": True,"headache_chronic_attack_lasting_three_to_seven_days": False,"headache_chronic_attack_lasting_up_to_five_minutes": False }
        elif slot_value == "Chronic, attack lasting three to seven days":
            return{"headache_duration":slot_value,"headache_chronic_attack_lasting_4_to_72_hours": False,"headache_chronic_attack_lasting_five_minutes_to_four_hours": False,"headache_chronic_attack_lasting_three_to_seven_days": True,"headache_chronic_attack_lasting_up_to_five_minutes": False  }
        elif slot_value == "Chronic, attack lasting up to five minutes":
            return{"headache_duration":slot_value,"headache_chronic_attack_lasting_4_to_72_hours": False,"headache_chronic_attack_lasting_five_minutes_to_four_hours": False,"headache_chronic_attack_lasting_three_to_seven_days": False,"headache_chronic_attack_lasting_up_to_five_minutes":True }

    def validate_headache_recent_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Recent, lasting for more than 1 hour and less than 1 day":
            return{"headache_recent_duration":slot_value,"headache_recent_lasting_for_more_than_1_hour_and_less_than_1_day": True,"headache_recent_lasting_less_than_1_hour": False,"headache_recent_lasting_more_than_1_day": False }
        elif slot_value == "Recent, lasting less than 1 hour":
            return{"headache_recent_duration":slot_value,"headache_recent_lasting_for_more_than_1_hour_and_less_than_1_day": False,"headache_recent_lasting_less_than_1_hour": True,"headache_recent_lasting_more_than_1_day": False }
        elif slot_value == "Recent, lasting more than 1 day":
            return{"headache_recent_duration":slot_value,"headache_recent_lasting_for_more_than_1_hour_and_less_than_1_day": False,"headache_recent_lasting_less_than_1_hour": False,"headache_recent_lasting_more_than_1_day": True }

    def validate_headache_pain_level(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Mild":
            return{"headache_pain_level":slot_value,"headache_mild":True}
        elif slot_value == "Moderate":
            return{"headache_pain_level":slot_value,"headache_moderate": True }
        elif slot_value == "Severe":
            return{"headache_pain_level":slot_value,"headache_severe": True}
    def validate_headache_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Forehead":
            return{"headache_location":slot_value,"headache_forehead":True,"headache_temporal_region": False,"headache_generalized": False}
        elif slot_value == "General":
            return{"headache_location":slot_value,"headache_generalized": True,"headache_forehead":False,"headache_temporal_region": False }
        elif slot_value == "At the temples":
            return{"headache_location":slot_value,"headache_temporal_region": True, "headache_generalized": False,"headache_forehead":False}
    def validate_headache_feeling(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Stabbing":
            return{"headache_feeling":slot_value,"headache_lancinating":True}
        elif slot_value == "Pressing":
            return{"headache_feeling":slot_value,"headache_pressing": True}
        elif slot_value == "Pulsating":
            return{"headache_feeling":slot_value,"headache_pulsating": True}

    def validate_headache_recent_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Recent, lasting for more than 1 hour and less than 1 day":
            return{"headache_recent_duration":slot_value,"headache_recent_lasting_for_more_than_1_hour_and_less_than_1_day": True,"headache_recent_lasting_less_than_1_hour": False,"headache_recent_lasting_more_than_1_day": False }
        elif slot_value == "Recent, lasting less than 1 hour":
            return{"headache_recent_duration":slot_value,"headache_recent_lasting_for_more_than_1_hour_and_less_than_1_day": False,"headache_recent_lasting_less_than_1_hour": True,"headache_recent_lasting_more_than_1_day": False }
        elif slot_value == "Recent, lasting more than 1 day":
            return{"headache_recent_duration":slot_value,"headache_recent_lasting_for_more_than_1_hour_and_less_than_1_day": False,"headache_recent_lasting_less_than_1_hour": False,"headache_recent_lasting_more_than_1_day": True }


    def validate_tremors_hands(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "One hand":
            return{"tremors_hands":slot_value,"tremors_both_hands":False,"tremors_in_one_hand": True}
        elif slot_value == "Both hands":
            return{"tremors_hands":slot_value,"tremors_both_hands": True,"tremors_in_one_hand": False}

    def validate_tremors_worsen(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Stress":
            return{"tremors_worsen":slot_value,"tremors_stress_related": True }
        elif slot_value == "Alcohol consumption":
            return{"tremors_worsen":slot_value,"tremors_subside_after_drinking_alcohol": True }
        elif slot_value == "Coffee/Tea consumption":
            return{"tremors_worsen":slot_value,"tremors_worsen_after_caffeine_intake":True }




class ValidateSkinForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_skin_form"
    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        all_slots = slots_mapped_in_domain

        if tracker.slots.get("dermatological_changes_entire_skin") == True:
            all_slots.remove("dermatological_changes_upper_lower_extremities")
            all_slots.remove("dermatological_changes_location")

        if tracker.slots.get("dermatological_changes_scalp") != True:
            all_slots.remove("dermatological_changes_localization_near_sebaceous_glands")

        if tracker.slots.get("dermatological_changes_located_in_the_genital_area") != True:
            all_slots.remove("erythema_foreskin_or_head_of_the_penis")
            all_slots.remove("dermatological_changes_located_in_genital_area_chancre")
            all_slots.remove("erythema_vulva")
        if tracker.slots.get("dermatological_changes_located_in_the_genital_area") == True and tracker.slots.get("gender") == "male":
            all_slots.remove("erythema_vulva")
        if tracker.slots.get("dermatological_changes_located_in_the_genital_area") == True and tracker.slots.get("gender") == "female":
            all_slots.remove("erythema_foreskin_or_head_of_the_penis")
        if tracker.slots.get("gender") == "male":
            all_slots.remove("dermatological_changes_recurring_during_infections_or_menstrual_period")
        if tracker.slots.get("dermatological_changes_located_on_the_face") != True:
            all_slots.remove("erythema_facial_butterfly_shaped")
        if tracker.slots.get("dermatological_changes_located_on_the_limb") != True:
            all_slots.remove("erythema_limb_hot_to_the_touch")

        if tracker.slots.get("pruritus") == False:
            all_slots.remove("pruritus_aggravated_by_change_in_temperature_sweating_or_wearing_wool") 
            all_slots.remove("pruritus_most_intense_at_night")

        if tracker.slots.get("skin_mass") == False:
            all_slots.remove("skin_mass_bleeding")
            all_slots.remove("skin_mass_greater_than_1_cm_in_diameter")

        if tracker.slots.get("dermatological_changes_painful") ==  False:
            all_slots.remove("skin_pain_severe")
        if tracker.slots.get("dermatological_changes_upper_lower_extremities") != "None":
            all_slots.remove("dermatological_changes_location")

        return all_slots

    def validate_dermatological_flare_ups_reason(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Coming into contact with buttons,fasteners or cosmetics":
            return{"dermatological_flare_ups_reason":slot_value,"dermatological_changes_at_the_point_of_contact_with_buttons_fasteners_or_cosmetics": True }
        elif slot_value == "Stress":
            return{"dermatological_flare_ups_reason":slot_value,"dermatological_changes_aggravated_by_stress": True }
        elif slot_value == "Alcohol consumption":
            return{"dermatological_flare_ups_reason":slot_value,"dermatological_changes_exacerbated_by_alcohol_consumption":True }
        elif slot_value == "Sunlight exposure":
            return{"dermatological_flare_ups_reason":slot_value,"dermatological_changes_exacerbated_by_sunlight_exposure":True }
        elif slot_value == "None of the above":
            return{"dermatological_flare_ups_reason": "Not affected by stress, alcohol, sunlight, or tight clothes"}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"dermatological_flare_ups_reason": None}

    def validate_dermatological_changes_located_in_the_genital_area(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == True:
            return{"dermatological_changes_located_in_the_genital_area": True}
        else:
            return{"dermatological_changes_located_in_the_genital_area": False, "dermatological_changes_female_genital_area": False,"dermatological_changes_male_genital_area": False }

    def validate_dermatological_changes_upper_lower_extremities(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        erythema_bool = tracker.slots.get("erythema")
        pruritus_bool = tracker.slots.get("pruritus")
        if slot_value == "Lower Body excluding feet":
            return{"dermatological_changes_upper_lower_extremities":slot_value,"dermatological_changes_lower_extremities_excluding_feet": True, "dermatological_changes_located_on_the_limb":True ,"erythema_limb":erythema_bool }
        elif slot_value == "Upper Body excluding hands":
            return{"dermatological_changes_upper_lower_extremities":slot_value,"dermatological_changes_upper_extremities_excluding_hands": True, "dermatological_changes_located_on_the_limb":True ,"erythema_limb":erythema_bool }
        elif slot_value == "Hand":
            return{"dermatological_changes_upper_lower_extremities": slot_value, "dermatological_changes_hands":True ,"erythema_hand":erythema_bool,"erythema_palmar":erythema_bool,"erythema_finger":erythema_bool, "dermatological_changes_located_on_the_limb":True ,"erythema_limb":erythema_bool}
        elif slot_value == "Feet":
            return{"dermatological_changes_upper_lower_extremities": slot_value,"dermatological_changes_feet": True ,"erythema_toe":erythema_bool,"pruritus_foot":pruritus_bool, "dermatological_changes_located_on_the_limb":True ,"erythema_limb":erythema_bool}
        elif slot_value == "Elsewhere":
            return{"dermatological_changes_upper_lower_extremities": "None"}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"dermatological_changes_upper_lower_extremities": None}
    
    def validate_dermatological_changes_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        erythema_bool = tracker.slots.get("erythema")
        pruritus_bool = tracker.slots.get("pruritus_bool")

        if slot_value == "Eyelid":
            return{"dermatological_changes_location":slot_value,"dermatological_changes_eyelid": True }
        elif slot_value == "Mouth":
            return{"dermatological_changes_location":slot_value,"dermatological_changes_located_in_the_mouth":True }
        elif slot_value == "Head/Face":
            return{"dermatological_changes_location":slot_value,"dermatological_changes_located_on_the_face":True,"erythema_facial": erythema_bool}
        elif slot_value == "Trunk":
            return{"dermatological_changes_location":slot_value,"dermatological_changes_trunk":True }
        elif slot_value == "Near a joint":
            return{"dermatological_changes_location":slot_value,"dermatological_changes_located_on_the_joint":True,"erythema_of_skin_overlying_a_joint": erythema_bool }
        elif slot_value == "Scalp":
            return{"dermatological_changes_location":slot_value,"dermatological_changes_scalp":True, "pruritus_scalp":pruritus_bool }
        elif slot_value == "Genitals":
            if tracker.slots.get("gender") == "male":
                return{"dermatological_changes_location": slot_value, "dermatological_changes_located_in_the_genital_area": True, "dermatological_changes_male_genital_area": True}
            else:
                return{"dermatological_changes_location": slot_value, "dermatological_changes_located_in_the_genital_area": True, "dermatological_changes_female_genital_area": True}
        elif slot_value == "other places" :
            return{"dermatological_changes_location": "Unknown" }
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"dermatological_changes_location": None}
  
    def validate_pigmentation(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "darken":
            return{"pigmentation": slot_value, "dermatological_changes_hyperpigmentation_of_the_skin": True}
        elif slot_value == "lighten":
            return{"pigmentation": slot_value, "hypopigmentation_of_the_skin": True}
        elif slot_value == "normal skin colour":
            return{"pigmentation": slot_value}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"pigmentation": None}

class ValidateJointForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_joint_form"
    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        all_slots = slots_mapped_in_domain

        if tracker.slots.get("joint_pain_ankle") == True:
            all_slots.remove("joint_pain_elbow")
            all_slots.remove("joint_pain_hallux")
            all_slots.remove("joint_pain_hip")
            all_slots.remove("joint_pain_knee")
            all_slots.remove("joint_pain_shoulder")
            all_slots.remove("joint_pain_thumb")
            all_slots.remove("joint_pain_wrist")
            all_slots.remove("joint_pain_others")
            all_slots.remove("joint_pain_during_elbow_movement")
            all_slots.remove("joint_pain_during_hip_movement")
            all_slots.remove("joint_pain_during_knee_movement")
            all_slots.remove("joint_pain_during_shoulder_movement")
            all_slots.remove("joint_pain_during_thumb_movement")
            all_slots.remove("joint_pain_during_wrist_movement")

        if tracker.slots.get("joint_pain_elbow") == True:
            all_slots.remove("joint_pain_ankle")
            all_slots.remove("joint_pain_hallux")
            all_slots.remove("joint_pain_hip")
            all_slots.remove("joint_pain_knee")
            all_slots.remove("joint_pain_shoulder")
            all_slots.remove("joint_pain_thumb")
            all_slots.remove("joint_pain_wrist")
            all_slots.remove("joint_pain_others")
            all_slots.remove("joint_pain_during_ankle_movement")
            all_slots.remove("joint_pain_during_hip_movement")
            all_slots.remove("joint_pain_during_knee_movement")
            all_slots.remove("joint_pain_during_shoulder_movement")
            all_slots.remove("joint_pain_during_thumb_movement")
            all_slots.remove("joint_pain_during_wrist_movement")

        if tracker.slots.get("joint_pain_hallux") == True:
            all_slots.remove("joint_pain_elbow")
            all_slots.remove("joint_pain_ankle")
            all_slots.remove("joint_pain_hip")
            all_slots.remove("joint_pain_knee")
            all_slots.remove("joint_pain_shoulder")
            all_slots.remove("joint_pain_thumb")
            all_slots.remove("joint_pain_wrist")
            all_slots.remove("joint_pain_others")
            all_slots.remove("joint_pain_during_elbow_movement")
            all_slots.remove("joint_pain_during_hip_movement")
            all_slots.remove("joint_pain_during_knee_movement")
            all_slots.remove("joint_pain_during_shoulder_movement")
            all_slots.remove("joint_pain_during_thumb_movement")
            all_slots.remove("joint_pain_during_wrist_movement")
            all_slots.remove("joint_pain_during_ankle_movement")

        if tracker.slots.get("joint_pain_hip") == True:
            all_slots.remove("joint_pain_elbow")
            all_slots.remove("joint_pain_hallux")
            all_slots.remove("joint_pain_ankle")
            all_slots.remove("joint_pain_knee")
            all_slots.remove("joint_pain_shoulder")
            all_slots.remove("joint_pain_thumb")
            all_slots.remove("joint_pain_wrist")
            all_slots.remove("joint_pain_others")
            all_slots.remove("joint_pain_during_elbow_movement")
            all_slots.remove("joint_pain_during_knee_movement")
            all_slots.remove("joint_pain_during_shoulder_movement")
            all_slots.remove("joint_pain_during_thumb_movement")
            all_slots.remove("joint_pain_during_wrist_movement")
            all_slots.remove("joint_pain_during_ankle_movement")

        if tracker.slots.get("joint_pain_knee") == True:
            all_slots.remove("joint_pain_elbow")
            all_slots.remove("joint_pain_hallux")
            all_slots.remove("joint_pain_hip")
            all_slots.remove("joint_pain_ankle")
            all_slots.remove("joint_pain_shoulder")
            all_slots.remove("joint_pain_thumb")
            all_slots.remove("joint_pain_wrist")
            all_slots.remove("joint_pain_others")
            all_slots.remove("joint_pain_during_elbow_movement")
            all_slots.remove("joint_pain_during_hip_movement")
            all_slots.remove("joint_pain_during_shoulder_movement")
            all_slots.remove("joint_pain_during_thumb_movement")
            all_slots.remove("joint_pain_during_wrist_movement")
            all_slots.remove("joint_pain_during_ankle_movement")

        if tracker.slots.get("joint_pain_shoulder") == True:
            all_slots.remove("joint_pain_elbow")
            all_slots.remove("joint_pain_hallux")
            all_slots.remove("joint_pain_hip")
            all_slots.remove("joint_pain_ankle")
            all_slots.remove("joint_pain_knee")
            all_slots.remove("joint_pain_thumb")
            all_slots.remove("joint_pain_wrist")
            all_slots.remove("joint_pain_others")
            all_slots.remove("joint_pain_during_elbow_movement")
            all_slots.remove("joint_pain_during_hip_movement")
            all_slots.remove("joint_pain_during_knee_movement")
            all_slots.remove("joint_pain_during_thumb_movement")
            all_slots.remove("joint_pain_during_wrist_movement")
            all_slots.remove("joint_pain_during_ankle_movement")

        if tracker.slots.get("joint_pain_thumb") == True:
            all_slots.remove("joint_pain_elbow")
            all_slots.remove("joint_pain_hallux")
            all_slots.remove("joint_pain_hip")
            all_slots.remove("joint_pain_ankle")
            all_slots.remove("joint_pain_shoulder")
            all_slots.remove("joint_pain_knee")
            all_slots.remove("joint_pain_wrist")
            all_slots.remove("joint_pain_others")
            all_slots.remove("joint_pain_during_elbow_movement")
            all_slots.remove("joint_pain_during_hip_movement")
            all_slots.remove("joint_pain_during_knee_movement")
            all_slots.remove("joint_pain_during_shoulder_movement")
            all_slots.remove("joint_pain_during_wrist_movement")
            all_slots.remove("joint_pain_during_ankle_movement")

        if tracker.slots.get("joint_pain_wrist") == True:
            all_slots.remove("joint_pain_elbow")
            all_slots.remove("joint_pain_hallux")
            all_slots.remove("joint_pain_hip")
            all_slots.remove("joint_pain_ankle")
            all_slots.remove("joint_pain_shoulder")
            all_slots.remove("joint_pain_thumb")
            all_slots.remove("joint_pain_knee")
            all_slots.remove("joint_pain_others")
            all_slots.remove("joint_pain_during_elbow_movement")
            all_slots.remove("joint_pain_during_hip_movement")
            all_slots.remove("joint_pain_during_knee_movement")
            all_slots.remove("joint_pain_during_shoulder_movement")
            all_slots.remove("joint_pain_during_thumb_movement")
            all_slots.remove("joint_pain_during_ankle_movement")


        if tracker.slots.get("joint_pain_others") == True:
            all_slots.remove("joint_pain_elbow")
            all_slots.remove("joint_pain_hallux")
            all_slots.remove("joint_pain_hip")
            all_slots.remove("joint_pain_ankle")
            all_slots.remove("joint_pain_shoulder")
            all_slots.remove("joint_pain_thumb")
            all_slots.remove("joint_pain_knee")
            all_slots.remove("joint_pain_wrist")
            all_slots.remove("joint_pain_during_elbow_movement")
            all_slots.remove("joint_pain_during_hip_movement")
            all_slots.remove("joint_pain_during_knee_movement")
            all_slots.remove("joint_pain_during_shoulder_movement")
            all_slots.remove("joint_pain_during_thumb_movement")
            all_slots.remove("joint_pain_during_wrist_movement")
            all_slots.remove("joint_pain_during_ankle_movement")

        if tracker.slots.get("joint_deformation_posttraumatic") == True:
            all_slots.remove("joint_deformation_nontraumatic")
        if tracker.slots.get("joint_deformation_nontraumatic") == True:
            all_slots.remove("joint_deformation_posttraumatic")

        return all_slots


    def validate_joint_pain_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Ankle":
            return{"joint_pain_location":slot_value,"joint_pain_ankle": True }
        elif slot_value == "Elbow":
            return{"joint_pain_location":slot_value,"joint_pain_elbow": True }
        elif slot_value == "Big toe":
            return{"joint_pain_location":slot_value,"joint_pain_hallux":True }
        elif slot_value == "Hip":
            return{"joint_pain_location":slot_value,"joint_pain_hip":True }
        elif slot_value == "Knee":
            return{"joint_pain_location":slot_value,"joint_pain_knee":True }
        elif slot_value == "Shoulder":
            return{"joint_pain_location":slot_value,"joint_pain_shoulder":True }
        elif slot_value == "Thumb":
            return{"joint_pain_location":slot_value,"joint_pain_thumb":True }
        elif slot_value == "Wrist":
            return{"joint_pain_location":slot_value,"joint_pain_wrist":True }
        elif slot_value == "Others":
            return{"joint_pain_location":slot_value,"joint_pain_others":True }

    def validate_joint_pain_trauma(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == True:
            return{"joint_pain_trauma":slot_value,"joint_deformation_posttraumatic": True }
        elif slot_value == False:
            return{"joint_pain_trauma":slot_value,"joint_deformation_nontraumatic": True }

class ValidateEarForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_ear_form"
    async def required_slots(
        self,
        slots_mapped_in_domain: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        all_slots = slots_mapped_in_domain
        if tracker.slots.get("decreased_hearing") == False:
            all_slots.remove("decreased_hearing_reason")
        if tracker.slots.get("discharge_from_ear") == False:
            all_slots.remove("discharge_from_ear_type")
        if tracker.slots.get("earache") == False:
            all_slots.remove("pain_increases_when_touching_ear_area")
            all_slots.remove("pain_behind_ear")
            
        return all_slots

    def validate_decreased_hearing_reason(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Sudden loss of hearing":
            return{"decreased_hearing":slot_value,"decreased_hearing_sudden_hearing_loss": True }
        elif slot_value == "Slowly losing hearing":
            return{"decreased_hearing":slot_value,"decreased_hearing_progressive_hearing_loss": True }
        elif slot_value == "Hearing ability changing (changing intensity and duration)":
            return{"decreased_hearing":slot_value,"decreased_hearing_variable_intensity_and_duration": True }

    def validate_discharge_from_ear_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Blood":
            return{"discharge_from_ear_type":slot_value,"discharge_from_ear_bloody": True }
        elif slot_value == "Pus":
            return{"discharge_from_ear_type":slot_value,"discharge_from_ear_purulent": True }
        elif slot_value == "Others":
            return{"discharge_from_ear_type":slot_value,"discharge_from_ear_others": True }

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

        if tracker.slots.get("eye_pain") == False:
            all_slots.remove("eye_pain_unbearable")
        if tracker.slots.get("impaired_vision") == False:
            all_slots.remove("impaired_vision_in_one_eye")
        if tracker.slots.get("impaired_eye_motion") == False:
            all_slots.remove("impaired_eye_motion_direction")
        if tracker.slots.get("eyelid_lesion") == False:
            all_slots.remove("eyelid_lesion_painful")
            all_slots.remove("eyelid_lesion_red_and_warm")
            all_slots.remove("eyelid_lesion_red_lump_with_yellow_tip")
        if tracker.slots.get("diplopia") == False:
            all_slots.remove("diplopia_lasting_more_than_24_hours")
        return all_slots

    def validate_impaired_eye_motion_direction(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value == "Moving Downwards":
            return{"impaired_eye_motion_direction":slot_value,"impaired_downward_eye_motion": True }
        elif slot_value == "Moving Upwards":
            return{"impaired_eye_motion_direction":slot_value,"impaired_upward_eye_motion": True }
        elif slot_value == "Moving to the left/right":
            return{"impaired_eye_motion_direction":slot_value,"impaired_lateral_eye_motion": True }
        elif slot_value == "Moving back to the centre":
            return{"impaired_eye_motion_direction":slot_value,"impaired_medial_eye_motion": True }
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"impaired_eye_motion_direction": None}

    def validate_eyelid_twitching(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"eyelid_twitching": True, "eyelid_tremors": True}
        elif slot_value == False:
            return {"eyelid_twitching": False, "eyelid_tremors": False}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"eyelid_twitching": None}

    def validate_diplopia_lasting_more_than_24_hours(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> Dict[Text, Any]:
        if slot_value:
            return {"diplopia_lasting_more_than_24_hours": True, "diplopia_lasting_up_to_24_hours": False}
        elif slot_value == False:
            return {"diplopia_lasting_more_than_24_hours": False, "diplopia_lasting_up_to_24_hours": True}
        else:
            dispatcher.utter_message(text = "Please select one of the options provided.")
            return {"diplopia_lasting_more_than_24_hours": None}
            
class SetSymptom(Action):

    def name(self) -> Text:
        return "action_set_symptom"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        symptom = tracker.get_intent_of_latest_message()
        all_slots = tracker.slots
        symptoms_list = []

        child_symptoms = {
            "cough_dry": "cough",
            "cough_productive": "cough",
            "hemoptysis": "cough",
            "abdominal_pain_crampy": "abdominal_pain",
            
        }

        for s in all_slots:
            symptoms_list.append(s)
        
        if symptom in symptoms_list:
            initial_evidence = tracker.get_slot("initial")
            
            if initial_evidence == None:
                initial_evidence = []

            if symptom == "cough_dry":
                initial_evidence.append("cough")
                initial_evidence


            initial_evidence.append(symptom.replace("_", " ").lower())
            return [SlotSet(symptom, True), SlotSet("initial", initial_evidence)]
        else:
            return []

class CreateReport(Action):
    def name(self) -> Text:
        return "action_create_report"

    def run(self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        history = {}
        report_present = {}
        report_absent = {}
        all_slots = tracker.slots

        history_slots = ["age", "gender", "allergy", "asthma"]
        
        for symptom in all_slots:
            if symptom in history_slots:
                history[symptom.replace("_", " ")] = tracker.slots.get(symptom)
            elif all_slots[symptom] == True:
                report_present[symptom.replace("_", " ")] = all_slots[symptom]
            elif isinstance(all_slots[symptom], str):
                report_present[symptom.replace("_", " ")] = all_slots[symptom]
            elif all_slots[symptom] == False:
                report_absent[symptom.replace("_", " ")] = all_slots[symptom]
            else:
                continue
        
        patient_hist = ["Patient:"]
        for h in history:
            if history[h] == True:
                patient_hist.append("{}: Yes".format(h))
            elif history[h] == False:
                patient_hist.append("{}: No".format(h))
            else:
                patient_hist.append("{}: {}".format(h, history[h]))

        chief_complaint = ["Chief complaint: "]
        initial_evidence = tracker.get_slot("initial")
        for s in initial_evidence:
            chief_complaint.append(s.replace("_", " "))

        present_symptoms = ["Symptoms Present: "]
        for i in report_present:
            if report_present[i] == True:
                present_symptoms.append(i)
            else:
                continue

        absent_symptoms = ["Symptoms Absent: "]
        for a in report_absent:
            absent_symptoms.append(a)

        symptom_list_df = pd.read_csv("actions/infermedica_symptom_list.csv")
        slots = tracker.slots
        age = tracker.get_slot("age")
        sex = tracker.get_slot("gender")
        evidence = []

        # Add initial evidence
        for i in initial_evidence:
            symptom_id = symptom_list_df.loc[symptom_list_df['symptom_name'] == i, "symptom_id"].iloc[0]
            if symptom_list_df['symptom_name'].eq(i).any():
                evidence.append({"id": symptom_id, "choice_id": "present", "source": "initial"})
        for s in slots:
            slot_name = s.replace("_", " ")
            if symptom_list_df['symptom_name'].eq(slot_name).any():
                print(slot_name)
                symptom_id = symptom_list_df.loc[symptom_list_df['symptom_name'] == slot_name, "symptom_id"].iloc[0]
                
                if slots[s] == True:
                    evidence.append({"id": symptom_id, "choice_id": "present"})
                else:
                    evidence.append({"id": symptom_id, "choice_id": "absent"})

        api = infermedica_api.APIv3Connector(app_id="fb1de113", app_key="97e9474d5049b2f276da86e8d16c1f6b")
        response = api.diagnosis(evidence=evidence, sex=sex, age=age)
        print(response)
        conditions = response["conditions"]
        triage = ["Associated Conditions: "]
        for i in range(len(conditions)):
            triage.append("{}, {}%".format(conditions[i]["name"], str(round(conditions[i]["probability"]*100, 2))))

        dispatcher.utter_message(text="\n".join(patient_hist))
        dispatcher.utter_message(text="\n".join(chief_complaint))
        dispatcher.utter_message(text="\n".join(present_symptoms))
        dispatcher.utter_message(text="\n".join(absent_symptoms))
        dispatcher.utter_message(text="\n".join(triage))

    
# class Neo4j:
#     def __init__(self, uri, user, password):
#         self.driver = gd.driver(uri, auth=(user, password))
        
#     def close(self):
#         self.driver.close()

#     def retrieve_disease_prob(self, symptom):
#         with self.driver.session() as session:
#             value = session.write_transaction(self._get_disease, symptom)
#             return value

#     @staticmethod
#     def _get_disease(tx, symptom):
#         diseases = {}
#         match = "(d:Disease)-[r]-(s:Symptom {{name: '{}'}})".format(symptom)
#         query = "MATCH {} RETURN d.name AS disease, r.probability AS prob".format(match)
        
#         result = tx.run(query)
#         for record in result:
#             diseases[record["disease"]] = record["prob"]
            
#         return diseases


# class CreateReport(Action):
#     def name(self) -> Text:
#         return "action_create_report"

#     def run(self,
#            dispatcher: CollectingDispatcher,
#            tracker: Tracker,
#            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         history = ["age", "gender", "allergy", "asthma", "eye_surgery", "diabetes"]
#         symptoms_to_present = [
#             "coughing",
#             "cough_type",
#             "phlegm_color",
#             "cough_duration",
#             "pain_when_coughing",
#             "persistent_cough",
#             "wheezing",
#             "shortness_of_breath",
#             "fever",
#             "temperature",
#             "fever_duration",
#             "feeling_cold",
#             "shivering",
#             "lethargy",
#             "stuffy_nose",
#             "runny_nose",
#             "nasal_congestion",
#             "nose_symptom_duration",
#             "facial_pain",
#             "headache",
#             "headache_location",
#             "headache_pain_scale",
#             "headache_type",
#             "headache_duration",
#             "head_injury",
#             "stress",
#             "dizziness",
#             "numbness",
#             "numbness_location",
#             "neck_pain",
#             "eye_symptom_location",
#             "eye_symptom_duration",
#             "eye_redness",
#             "eye_pain",
#             "eye_pain_scale",
#             "eye_injury",
#             "eye_discharge",
#             "blurred_vision",
#             "double_vision",
#             "sensitivity_to_light",
#             "photopsia",
#             "photopsia_location",
#             "vision_loss",
#             "floaters",
#             "contact_lens",
#             "abdominal_pain",
#             "abdominal_pain_location",
#             "abdominal_symptom_duration",
#             "abdominal_pain_scale",
#             "abdominal_tenderness",
#             "abdominal_distension",
#             "stomach_cramps",
#             "diarrhea",
#             "constipation",
#             "loss_of_appetite",
#             "flank_pain",
#             "blood_in_stool",
#             "blood_in_urine",
#             "dark_urine",
#             "pain_during_urination",
#             "nausea",
#             "vomiting",
#             "yellow_skin_and_eyes"
#             ]
#         symptoms_in_database = [
#             'hoarseness',
#             'restless legs syndrome',
#             'enlarged neck lymph nodes',
#             'physical deformity',
#             'erectile dysfunction',
#             'vision loss',
#             'abdominal discomfort',
#             'skin lesion',
#             'anger',
#             'pain',
#             'muscle weakness',
#             'urinary retention',
#             'heavy or prolonged periods',
#             'scar',
#             'fluid in the lungs',
#             'neck swelling',
#             'severe headache',
#             'chills',
#             'memory loss',
#             'foot pain',
#             'racing thoughts',
#             'slow heart rate',
#             'itchy eyes',
#             'pain during urination',
#             'elbow pain',
#             'sleepiness',
#             'abdominal tenderness',
#             'ear pain',
#             'abdominal pain',
#             'pain in upper-right abdomen',
#             'shakiness',
#             'skin irritation',
#             'peeling skin',
#             'gagging',
#             'ache',
#             'scarring within the bile ducts',
#             'discomfort',
#             'sweating',
#             'flank pain',
#             'arm pain',
#             'dull pain',
#             'dark urine',
#             'seizures',
#             'headache',
#             'hearing voices',
#             'wandering and getting lost',
#             'weakness of one side of the body',
#             'plaque',
#             'oral thrush',
#             'slow bodily movement',
#             'raised area of skin',
#             'hopelessness',
#             'weakness',
#             'clumsiness',
#             'bowel obstruction',
#             'rash on the face',
#             'knee pain',
#             'lower abdominal pain',
#             'wrist pain',
#             'regurgitation',
#             'episodes of no breathing',
#             'persistent cough',
#             'heel pain',
#             'limping',
#             'leg numbness',
#             'malnutrition',
#             'shoulder pain',
#             'manic episode',
#             'sensitivity to sound',
#             'severe anxiety',
#             'falling',
#             'asymmetry',
#             'swollen knee',
#             'neck pain',
#             'hunger',
#             'difficulty swallowing',
#             'forgetfulness',
#             'abnormality walking',
#             'feeling cold',
#             'drooling',
#             'wheezing',
#             'sensitivity to light',
#             'delusion',
#             'aggression',
#             'bruising',
#             'heat therapy',
#             'ice pack',
#             'jaw pain',
#             'chest pain worsened by breathing',
#             'decreased range of motion',
#             'flushing',
#             'slurred speech',
#             'hand swelling',
#             'skin rash',
#             'rectal pain',
#             'failure to thrive',
#             'heartburn',
#             'arm discomfort',
#             'stomach cramps',
#             'difficulty speaking',
#             'coma',
#             'mild pain',
#             'discomfort in upper abdomen',
#             'itching',
#             'severe pain',
#             'hand tremor',
#             'irregular menstruation',
#             'chronic back pain',
#             'brief visual or sensory abnormality',
#             'head congestion',
#             'drooping of upper eyelid',
#             'sharp pain',
#             'paranoia',
#             'phlegm',
#             'fluid in the abdomen',
#             'pins and needles',
#             'hip pain',
#             'incontinence',
#             'fatigue',
#             'stiff neck',
#             'impaired voice',
#             'racing heartbeat',
#             'shortness of breath',
#             'radiating pain',
#             'swelling under the skin',
#             'unequal pupils',
#             'pimple',
#             'facial swelling',
#             'eye pain',
#             'blurred vision',
#             'pain in right lower abdomen',
#             'facial pain',
#             'swollen feet',
#             'fever',
#             'inability to feel pleasure',
#             'sinus pain',
#             'dehydration',
#             'weight loss',
#             'persistent headache',
#             'guilt',
#             'thoughts of suicide',
#             'kidney failure',
#             'eye redness',
#             'bleeding from anus',
#             'tongue swelling',
#             'pelvic pain',
#             'stinging sensation',
#             'cyst',
#             'difficulty with bodily movement',
#             'face rash',
#             'leg pain',
#             'shivering',
#             'dark stool from digested blood',
#             'diarrhea',
#             'low oxygen in the body',
#             'poor appetite',
#             'lesion',
#             'noisy breathing',
#             'chest tightness',
#             'agitation',
#             'ringing in the ears',
#             'paralysis',
#             'amnesia',
#             'partial loss of vision',
#             'yellow skin and eyes',
#             'finger pain',
#             'screaming',
#             'cloudy urine',
#             'fear of loud sounds',
#             'muscle spasms',
#             'eye discharge',
#             'swelling of the surface of the eye',
#             'acute episodes',
#             'lower extremity pain',
#             'lump',
#             'blister',
#             'vomiting',
#             'blood in urine',
#             'hallucination',
#             'unsteady gait',
#             'fainting',
#             'restlessness',
#             'back pain',
#             'joint pain',
#             'dizziness',
#             'upper abdominal pain',
#             'leg pain during exercise',
#             'painful swallowing',
#             'coughing up blood',
#             'feeling tired',
#             'confusion in the evening hours',
#             'sneezing',
#             'laryngitis',
#             'indigestion',
#             'dryness',
#             'bleeding',
#             'high fever',
#             'watery eyes',
#             'swollen joint',
#             'fast breathing',
#             'double vision',
#             'swollen veins in the lower esophagus',
#             'nightmares',
#             'muscle twitches',
#             'tremor at rest',
#             'substance abuse',
#             'lump on the skin or joint',
#             'disorganized behavior',
#             'infection',
#             'watery diarrhea',
#             'muscle pain',
#             'collapse',
#             'unsteadiness',
#             'visual hallucinations',
#             'abdominal cramping from gallstones',
#             'increased thirst',
#             'frequent urge to urinate',
#             'foot numbness',
#             'fear',
#             'frequent urination',
#             'hand pain',
#             'swollen tonsils',
#             'lightheadedness',
#             'lethargy',
#             'vision disorder',
#             'throbbing pain',
#             'vaginal pain',
#             'mild cough',
#             'cough with phlegm',
#             'intermittent pain',
#             'runny nose',
#             'nasal congestion',
#             'pain worse at rest',
#             'coughing',
#             'red spots',
#             'loss of interest',
#             'anxiety',
#             'discharge from penis',
#             'eye irritation',
#             'slowness in activity and thought',
#             'difficulty breathing',
#             'panic attack',
#             'swollen lymph nodes',
#             'leaked fluid out of blood vessels or an organ',
#             'sadness',
#             'red rashes',
#             'scab',
#             'dry skin',
#             'belching',
#             'toe pain',
#             'difficulty walking',
#             'dry cough',
#             'blotchy rash',
#             'cramping',
#             'chest discomfort',
#             'crying',
#             'impulsivity',
#             'mood swings',
#             'chest pressure',
#             'low body temperature',
#             'spotting',
#             'elevated alkaline phosphatase',
#             'sinus pressure',
#             'trembling',
#             'mental confusion',
#             'inflammation of ear',
#             'foul smelling urine',
#             'pain in lower abdomen',
#             'shortness of breath while lying down',
#             'vomiting blood',
#             'intermittent abdominal pain',
#             'swelling in extremities',
#             'bone loss',
#             'nerve pain',
#             'throbbing headache',
#             'ankle pain',
#             'disorientation',
#             'low blood pressure',
#             'problems with coordination',
#             'irritation of the tonsils',
#             'weight gain',
#             'thirst',
#             'pain in upper abdomen',
#             'loss of appetite',
#             'rapid involuntary eye movement',
#             'blood in stool',
#             'fast heart rate',
#             'vertigo',
#             'tremor',
#             'tenderness',
#             'difficulty concentrating',
#             'excess thirst',
#             'nausea',
#             'tongue numbness',
#             'rib pain',
#             'respiratory distress',
#             'depression',
#             'burning sensation',
#             'delirium',
#             'insomnia',
#             'vaginal discharge',
#             'swelling',
#             'stiffness',
#             'side pain',
#             'seeing spots',
#             'abdominal distension',
#             'numbness',
#             'sore throat',
#             'vaginal bleeding',
#             'chronic cough',
#             'difficulty raising the foot',
#             'flapping tremor',
#             'redness',
#             'dry mouth',
#             'constipation',
#             'hand numbness',
#             'pain when coughing',
#             'groin pain',
#             'snoring',
#             'confusion',
#             'iron deficiency',
#             'calf pain',
#             'testicle pain',
#             'leaking of urine',
#             'malaise',
#             'night sweats',
#             'excess urination',
#             'stuffy nose',
#             'facial paralysis',
#             'cavity'
#             ]
#         def get_diagnosis(symptoms):
#             cyberlife_db = Neo4j("neo4j+s://ec6b6187.databases.neo4j.io:7687", "neo4j", "03u6rStifaqB7A-aOVXqttceAMzs-LuD7P19eK_l_yQ")
#             diagnosis = {}
#             for s in symptoms:
#                 d = cyberlife_db.retrieve_disease_prob(s)
#                 for key in d:
#                     if key in diagnosis:
#                         diagnosis[key] = diagnosis[key] + d[key]
#                     else:
#                         diagnosis[key] = d[key]
            
#             return sorted(diagnosis, key=diagnosis.get, reverse=True)[:3]
#         all_slots = tracker.slots
#         report_slots = {}
#         hist = []
#         present = []
#         absent = []
#         symptoms_to_diagnose = []
#         top3 = ["Possible Causes:"]
#         for s in all_slots:
#             if all_slots[s] == None:
#                 continue
#             elif all_slots[s] == False:
#                 if s in symptoms_to_present:
#                     absent.append(s.replace("_", " "))
#             else:
#                 if s in history and all_slots[s] == True:
#                     w = "{}: {}".format(s.replace("_", " "),"Yes")
#                     hist.append(w)
#                 elif s in history and all_slots[s] == False:
#                     w = "{}: {}".format(s.replace("_", " "),"No")
#                     hist.append(w)
#                 elif s in history:
#                     w = "{}: {}".format(s.replace("_", " "),all_slots[s])
#                     hist.append(w)
#                 else:
#                     if s in symptoms_to_present:
#                         report_slots[s] = all_slots[s]
        
#         for symptom in report_slots:
#             if symptom[-8:] == "duration":
#                 dur = "\t- Time since onset: " + report_slots[symptom]
#                 present.append(dur)
#             elif symptom[-5:] == "scale":
#                 scale = "\t- Intensity: " + report_slots[symptom]
#                 present.append(scale)
#             elif symptom[-8:] == "location":
#                 loc = "\t- Location: " + report_slots[symptom]
#                 present.append(loc)
#             elif report_slots[symptom] == True:
#                 present.append(symptom.replace("_", " "))
#             else:
#                 w = "{}: {}".format(symptom.replace("_", " "),report_slots[symptom])
#                 present.append(w)

#             if symptom.replace("_", " ") in symptoms_in_database:
#                 symptoms_to_diagnose.append(symptom.replace("_", " "))
        
#         top3 = top3 + get_diagnosis(symptoms_to_diagnose)
#         report = hist + ["Present:"] + present + ["Absent:"] + absent + top3
#         dispatcher.utter_message(text = "\n".join(report))
#         print("\n".join(report))
#         return []
