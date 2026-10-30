# Made by Ahmed Elrewiny
import time
from datetime import datetime, timedelta
from itertools import count


class TimeSlot:
    def __init__(self, time_slot_id, start_time, end_time):
        self._time_slot_id = time_slot_id
        self._start_time = start_time
        self._end_time = end_time
        self._is_booked = False

    @property
    def time_slot_id(self):
        return self._time_slot_id

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def is_booked(self):
        return self._is_booked

    def is_available(self):
        return not self._is_booked

    def mark_as_booked(self):
        self._is_booked = True

    def release(self):
        """Make the slot available again (used when an appointment is declined)."""
        self._is_booked = False

    def __str__(self):
        return (f"Slot {self._time_slot_id}: "
                f"{self._start_time:%a %d %b %Y, %H:%M} - {self._end_time:%H:%M}")


class Appointment:
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    DECLINED = "Declined"

    _id_counter = count(1)

    def __init__(self, patient, doctor, time_slot):
        self._appointment_id = next(Appointment._id_counter)
        self._status = Appointment.PENDING
        self._booked_at = None
        self._patient = patient
        self._doctor = doctor
        self._time_slot = time_slot

    @property
    def appointment_id(self):
        return self._appointment_id

    @property
    def status(self):
        return self._status

    @property
    def booked_at(self):
        return self._booked_at

    @property
    def patient(self):
        return self._patient

    @property
    def doctor(self):
        return self._doctor

    @property
    def time_slot(self):
        return self._time_slot

    def book(self):
        """Sequence diagram step: Appointment checks the TimeSlot and books it.
        The appointment stays Pending until the doctor accepts or declines it."""
        if self._time_slot.is_available():
            self._time_slot.mark_as_booked()
            self._booked_at = datetime.now()
            return "BOOKING_CONFIRMED"
        return "BOOKING_FAILED"

    def accept(self):
        """Accept the appointment. Returns True only if it was Pending."""
        if self._status != Appointment.PENDING:
            return False
        self._status = Appointment.ACCEPTED
        return True

    def decline(self):
        """Decline the appointment and release its slot.
        Returns True only if it was Pending; otherwise nothing changes."""
        if self._status != Appointment.PENDING:
            return False
        self._status = Appointment.DECLINED
        self._time_slot.release()
        # Simulated console notification (not a real delivered notification).
        print(f"  [Notification to {self._patient.name}] Your appointment with "
              f"Dr. {self._doctor.name} on "
              f"{self._time_slot.start_time:%a %d %b %Y, %H:%M} was declined.")
        return True

    def __str__(self):
        return (f"Appointment #{self._appointment_id} [{self._status}] - "
                f"{self._patient.name} with Dr. {self._doctor.name}, {self._time_slot}")


class Doctor:
    def __init__(self, doctor_id, name, specialization):
        self._doctor_id = doctor_id
        self._name = name
        self._specialization = specialization
        self._time_slots = []      # Doctor provides TimeSlots (composition)
        self._appointments = []    # Doctor has Appointments

    @property
    def name(self):
        return self._name

    @property
    def specialization(self):
        return self._specialization

    def add_time_slot(self, time_slot):
        self._time_slots.append(time_slot)

    def add_appointment(self, appointment):
        self._appointments.append(appointment)

    def get_available_time_slots(self):
        now = datetime.now()
        return [s for s in self._time_slots
                if s.is_available() and s.start_time > now]

    def accept_appointment(self, appointment):
        if appointment.doctor is not self:
            print("  Error: this appointment belongs to another doctor.")
            return False
        if not appointment.accept():
            print(f"  Error: appointment #{appointment.appointment_id} "
                  f"is already {appointment.status} and cannot be processed again.")
            return False
        return True

    def decline_appointment(self, appointment):
        if appointment.doctor is not self:
            print("  Error: this appointment belongs to another doctor.")
            return False
        if not appointment.decline():
            print(f"  Error: appointment #{appointment.appointment_id} "
                  f"is already {appointment.status} and cannot be processed again.")
            return False
        return True


class Patient:
    MAX_UPCOMING_APPOINTMENTS = 4

    def __init__(self, patient_id, name, email):
        self._patient_id = patient_id
        self._name = name
        self._email = email
        self._appointments = []
        self.last_result = None    # result code of the latest booking attempt

    @property
    def name(self):
        return self._name

    def get_upcoming_appointments(self):
        """Pending or Accepted appointments whose time has not passed yet."""
        now = datetime.now()
        return [a for a in self._appointments
                if a.status != Appointment.DECLINED and a.time_slot.start_time > now]

    def book_appointment(self, doctor, slot):
        # 1. Enforce the limit of 4 upcoming appointments (R4)
        if len(self.get_upcoming_appointments()) >= Patient.MAX_UPCOMING_APPOINTMENTS:
            self.last_result = "BOOKING_REJECTED_LIMIT_REACHED"
            return None

        # 2. The slot must be among the doctor's available slots (R1, R2)
        if slot not in doctor.get_available_time_slots():
            self.last_result = "BOOKING_REJECTED_SLOT_UNAVAILABLE"
            return None

        # 3. Appointment asks the TimeSlot to confirm and book itself
        appointment = Appointment(self, doctor, slot)
        self.last_result = appointment.book()
        if self.last_result != "BOOKING_CONFIRMED":
            return None

        self._appointments.append(appointment)
        doctor.add_appointment(appointment)
        return appointment


def main():
    print("=== Clinic Appointments System Demo ===\n")

    # --- Create patients and doctor ---
    sara = Patient(1, "Sara", "sara@example.com")
    omar = Patient(2, "Omar", "omar@example.com")
    doctor = Doctor(1, "Ahmed Hassan", "Cardiology")

    # --- Create time slots (one hour each, starting tomorrow at 09:00) ---
    base = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
    slots = []
    for i in range(6):
        start = base + timedelta(days=i)
        slot = TimeSlot(i + 1, start, start + timedelta(hours=1))
        doctor.add_time_slot(slot)
        slots.append(slot)

    # --- R1 / R6: retrieve and display available slots, and time it ---
    print(f"1) Available time slots for Dr. {doctor.name}:")
    start_timer = time.perf_counter()
    available = doctor.get_available_time_slots()
    for s in available:
        print("   ", s)
    elapsed = time.perf_counter() - start_timer
    print(f"    Retrieve + display time: {elapsed:.6f} seconds (R6 limit: 2 seconds)")
    print("    Note: this is a single in-memory measurement on this machine; it does")
    print("    not prove R6 would hold with real data, a database, or many users.")

    # --- Successful booking request ---
    print("\n2) Sara requests slot 1:")
    appt1 = sara.book_appointment(doctor, slots[0])
    print("   Result:", sara.last_result)
    print("   ", appt1)

    # --- Slot already booked ---
    print("\n3) Omar requests slot 1 (already booked):")
    result = omar.book_appointment(doctor, slots[0])
    print("   Result:", omar.last_result)
    print("   Appointment created:", result is not None)

    # --- Fill Sara's limit, one attempt at a time ---
    print("\n4) Sara requests slot 2:")
    appt2 = sara.book_appointment(doctor, slots[1])
    print("   Result:", sara.last_result)
    print("   ", appt2)

    print("\n5) Sara requests slot 3:")
    appt3 = sara.book_appointment(doctor, slots[2])
    print("   Result:", sara.last_result)
    print("   ", appt3)

    print("\n6) Sara requests slot 4:")
    appt4 = sara.book_appointment(doctor, slots[3])
    print("   Result:", sara.last_result)
    print("   ", appt4)
    print("    Sara's upcoming appointments:", len(sara.get_upcoming_appointments()))

    # --- Limit reached ---
    print("\n7) Sara requests slot 5 (limit of 4 reached):")
    result = sara.book_appointment(doctor, slots[4])
    print("   Result:", sara.last_result)
    print("   Appointment created:", result is not None)

    # --- R3: doctor accepts / declines ---
    print(f"\n8) Doctor accepts appointment #{appt1.appointment_id}:")
    ok = doctor.accept_appointment(appt1)
    print("   Success:", ok)
    print("   ", appt1)

    print(f"\n9) Doctor declines appointment #{appt2.appointment_id}:")
    ok = doctor.decline_appointment(appt2)
    print("   Success:", ok)
    print("   ", appt2)
    print("    Slot 2 is booked?", slots[1].is_booked)

    # --- Already processed appointments cannot be processed again ---
    print(f"\n10) Doctor tries to decline the already accepted appointment #{appt1.appointment_id}:")
    ok = doctor.decline_appointment(appt1)
    print("   Success:", ok)
    print("   ", appt1)
    print("    Slot 1 still booked?", slots[0].is_booked)

    print(f"\n11) Doctor tries to accept the already declined appointment #{appt2.appointment_id}:")
    ok = doctor.accept_appointment(appt2)
    print("   Success:", ok)
    print("   ", appt2)

    # --- Declined slot becomes available again ---
    print("\n12) Available slots after the decline:")
    for s in doctor.get_available_time_slots():
        print("   ", s)

    print("\n13) Omar requests the released slot 2:")
    appt5 = omar.book_appointment(doctor, slots[1])
    print("   Result:", omar.last_result)
    print("   ", appt5)

    print("\n14) Sara's upcoming appointments (declined ones don't count):")
    for a in sara.get_upcoming_appointments():
        print("   ", a)
    print("    Count:", len(sara.get_upcoming_appointments()))

    print("\n=== Demo finished ===")


if __name__ == "__main__":
    main()