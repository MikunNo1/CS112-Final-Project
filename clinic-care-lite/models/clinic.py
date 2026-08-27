import json
import os


class Clinic:
    def __init__(self, clinic_id, name, clinician_id):
        self.clinic_id = str(clinic_id)
        self.name = name
        self.clinician_id = str(clinician_id)
        self.patient_ids = []

    def add_patient(self, patient_id):
   
        patient_id = str(patient_id)

        if patient_id in self.patient_ids:
            raise ValueError("Patient is already registered with this clinic.")

        self.patient_ids.append(patient_id)

    def remove_patient(self, patient_id):

        patient_id = str(patient_id)

        if patient_id not in self.patient_ids:
            raise ValueError("Patient is not registered with this clinic.")

        self.patient_ids.remove(patient_id)

    def has_patient(self, patient_id):

        return str(patient_id) in self.patient_ids

    def save(self):

        os.makedirs(os.path.dirname(self.FILE_PATH), exist_ok=True)

        if not os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "w") as f:
                json.dump({}, f, indent=4)

        
        with open(self.FILE_PATH, "r") as f:
            data = json.load(f)

       
        data[self.clinic_id] = {
            "name": self.name,
            "clinician_id": self.clinician_id,
            "patient_ids": self.patient_ids
        }

       
        with open(self.FILE_PATH, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load(cls, clinic_id):
        
        clinic_id = str(clinic_id)

        with open(cls.FILE_PATH, "r") as f:
            data = json.load(f)

        if clinic_id not in data:
            return None

        clinic_data = data[clinic_id]

        clinic = cls(
            clinic_id=clinic_id,
            name=clinic_data["name"],
            clinician_id=clinic_data["clinician_id"]
        )

        clinic.patient_ids = clinic_data.get("patient_ids", [])

        return clinic

    @classmethod
    def get_all(cls):

        with open(cls.FILE_PATH, "r") as f:
            data = json.load(f)

        clinics = []

        for clinic_id, clinic_data in data.items():

            clinic = cls(
                clinic_id=clinic_id,
                name=clinic_data["name"],
                clinician_id=clinic_data["clinician_id"]
            )

            clinic.patient_ids = clinic_data.get("patient_ids", [])

            clinics.append(clinic)

        return clinics

    @classmethod
    def get_by_clinician(cls, clinician_id):

        clinician_id = str(clinician_id)

        clinics = cls.get_all()

        return [
            clinic
            for clinic in clinics
            if clinic.clinician_id == clinician_id
        ]

    @classmethod
    def get_patient_clinic(cls, patient_id):

        patient_id = str(patient_id)

        clinics = cls.get_all()

        for clinic in clinics:
            if clinic.has_patient(patient_id):
                return clinic

        return None

    def save_patient_changes(self):

        self.save()

    def __repr__(self):

        return (
            f"Clinic("
            f"id={self.clinic_id}, "
            f"name={self.name!r}, "
            f"clinician={self.clinician_id}, "
            f"patients={len(self.patient_ids)}"
            f")"
        )
