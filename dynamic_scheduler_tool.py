import json
import os
import datetime
import calendar
from typing import List, Dict, Any, Optional, Callable
from collections import defaultdict
import random

# =============================================================================
# 1. Dynamic Entity Definition
# =============================================================================

class Entity:
    """
    Base class for entities like Person, Department, Activity.  Provides
    basic ID management and string representation.
    """
    _next_id = 1

    def __init__(self, name: str, entity_type: str):
        """
        Initialize an Entity object.

        Args:
            name (str): The name of the entity.
            entity_type (str): The type of the entity (e.g., "Person", "Department").
        """
        self.id = Entity._next_id
        Entity._next_id += 1
        self.name = name
        self.entity_type = entity_type

    def __str__(self) -> str:
        """
        Returns a string representation of the entity.
        """
        return f"{self.entity_type} {self.id}: {self.name}"

    def __repr__(self) -> str:
        """Official string representation for developers (useful for debugging)."""
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}', type='{self.entity_type}')"


class Person(Entity):
    """
    Represents a person with attributes like skills, availability, and preferences.
    """
    def __init__(self, name: str, skills: List[str] = None, availability: Dict[str, List[str]] = None, preferences: Dict[str, int] = None):
        """
        Initialize a Person object.

        Args:
            name (str): The name of the person.
            skills (List[str], optional): A list of skills the person possesses. Defaults to [].
            availability (Dict[str, List[str]], optional): A dictionary representing the person's availability
                (e.g., {"Monday": ["9:00-17:00"], "Tuesday": ["10:00-18:00"]}). Defaults to {}.
            preferences (Dict[str, int], optional): A dictionary representing the person's preferences
                for certain tasks or times (e.g., {"Task1": 5, "Morning": 3}).  Higher is better. Defaults to {}.
        """
        super().__init__(name, "Person")
        self.skills = skills if skills is not None else []
        self.availability = availability if availability is not None else {}
        self.preferences = preferences if preferences is not None else {}

    def __str__(self) -> str:
        """
        Returns a string representation of the person.
        """
        return f"{super().__str__()} (Skills: {', '.join(self.skills)})"

    def __repr__(self) -> str:
        """Official string representation for developers."""
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}', skills={self.skills}, availability={self.availability}, preferences={self.preferences})"


class Department(Entity):
    """
    Represents a department with a name and optionally, associated people.
    """
    def __init__(self, name: str, people: List[Person] = None):
        """
        Initialize a Department object.

        Args:
            name (str): The name of the department.
            people (List[Person], optional): A list of Person objects belonging to the department. Defaults to [].
        """
        super().__init__(name, "Department")
        self.people = people if people is not None else []

    def __str__(self) -> str:
        """
        Returns a string representation of the department.
        """
        return f"{super().__str__()} (Employees: {len(self.people)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}', people={[p.id for p in self.people]})"


class Activity(Entity):
    """
    Represents an activity or task that needs to be scheduled.
    """
    def __init__(self, name: str, required_skills: List[str] = None, duration: int = 1, start_time: Optional[str] = None, end_time: Optional[str] = None, location: Optional[str] = None):
        """
        Initialize an Activity object.

        Args:
            name (str): The name of the activity.
            required_skills (List[str], optional): A list of skills required to perform the activity. Defaults to [].
            duration (int, optional): The duration of the activity in hours. Defaults to 1.
            start_time (Optional[str], optional): The earliest start time for the activity (e.g., "09:00"). Defaults to None.
            end_time (Optional[str], optional): The latest end time for the activity (e.g., "17:00"). Defaults to None.
            location (Optional[str], optional): The location where the activity takes place. Defaults to None.
        """
        super().__init__(name, "Activity")
        self.required_skills = required_skills if required_skills else []
        self.duration = duration
        self.start_time = start_time
        self.end_time = end_time
        self.location = location

    def __str__(self) -> str:
        """
        Returns a string representation of the activity.
        """
        details = [f"Duration: {self.duration} hours"]
        if self.start_time:
            details.append(f"Start: {self.start_time}")
        if self.end_time:
            details.append(f"End: {self.end_time}")
        if self.location:
            details.append(f"Location: {self.location}")
        if self.required_skills:
            details.append(f"Skills: {', '.join(self.required_skills)}")
        return f"{super().__str__()} ({', '.join(details)})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, name='{self.name}', required_skills={self.required_skills}, duration={self.duration}, start_time='{self.start_time}', end_time='{self.end_time}', location='{self.location}')"



# =============================================================================
# 2. Monthly Schedule Generation
# =============================================================================

class ScheduleGenerator:
    """
    Generates a schedule for a given month and year based on entities
    (persons, activities) and simple rules.
    """
    def __init__(self, entities: Dict[str, List[Entity]]):
        """
        Initialize the ScheduleGenerator with entities.

        Args:
            entities (Dict[str, List[Entity]]): A dictionary of entities, where keys are entity types
                (e.g., "Person", "Activity") and values are lists of entities.
        """
        self.entities = entities
        self.schedule = {}  # Will store the generated schedule

    def generate_monthly_schedule(self, year: int, month: int, algorithm: str = 'round_robin') -> Dict[str, Dict[str, List[Dict[str, Any]]]]:
        """
        Generates a monthly schedule.

        Args:
            year (int): The year for which to generate the schedule.
            month (int): The month for which to generate the schedule (1-12).
            algorithm (str, optional): The scheduling algorithm to use.  Currently supports 'round_robin'
                and 'availability_match'. Defaults to 'round_robin'.

        Returns:
            Dict[str, Dict[str, List[Dict[str, Any]]]]: A dictionary representing the schedule.  The outer key is the date
                (e.g., "2024-01-01"), the inner key is the shift or time slot (e.g., "Morning", "Afternoon", "09:00-17:00"),
                and the value is a list of activities scheduled for that time slot.  The activities
                are represented as dictionaries.  Returns an empty dict if no schedule is generated.
        """
        self.schedule = {}  # Clear any previous schedule
        if not self.entities.get("Person") or not self.entities.get("Activity"):
            print("Cannot generate schedule: No Person or Activity entities provided.")
            return {}

        # Get the number of days in the specified month
        _, num_days = calendar.monthrange(year, month)

        # Create a list of dates for the month
        dates = [datetime.date(year, month, day) for day in range(1, num_days + 1)]

        if algorithm == 'round_robin':
            self._generate_round_robin_schedule(dates)
        elif algorithm == 'availability_match':
            self._generate_availability_match_schedule(dates)
        else:
            print(f"Error: Unknown scheduling algorithm '{algorithm}'.  Using round-robin.")
            self._generate_round_robin_schedule(dates)  # Fallback to round-robin

        return self.schedule

    def _generate_round_robin_schedule(self, dates: List[datetime.date]) -> None:
        """
        Generates a schedule using a round-robin algorithm.  Assigns activities to people
        in a rotating fashion.

        Args:
            dates (List[datetime.date]): A list of dates for which to generate the schedule.
        """
        people = self.entities["Person"]
        activities = self.entities["Activity"]
        num_people = len(people)
        num_activities = len(activities)
        if num_people == 0:
            return  # No people, nothing to schedule

        person_index = 0
        for date in dates:
            date_str = date.strftime("%Y-%m-%d")
            self.schedule[date_str] = {"Morning": [], "Afternoon": [], "Evening": []}  # Basic shifts.  Extend as needed.
            for i in range(num_activities):
                activity = activities[i]
                person = people[person_index % num_people]  # Use modulo to cycle through people
                shift = ["Morning", "Afternoon", "Evening"][i % 3] # simple shift assignment
                self.schedule[date_str][shift].append({"activity": activity, "person": person})
                person_index += 1

    def _generate_availability_match_schedule(self, dates: List[datetime.date]) -> None:
        """
        Generates a schedule by trying to match person availability to activity times.
        This is a *very* basic example and would need significant expansion for real-world use.

        Args:
            dates (List[datetime.date]): A list of dates for which to generate the schedule.
        """
        people = self.entities["Person"]
        activities = self.entities["Activity"]
        for date in dates:
            date_str = date.strftime("%Y-%m-%d")
            self.schedule[date_str] = {"Morning": [], "Afternoon": [], "Evening": []}
            for activity in activities:
                # Very basic matching:  Can *anyone* work at this time?
                available_people = []
                for person in people:
                    day_of_week = date.strftime("%A")  # e.g., "Monday"
                    if day_of_week in person.availability:
                        # Check if the activity's time window overlaps with the person's availability
                        for available_time_range in person.availability[day_of_week]:
                            start, end = available_time_range.split("-")  # e.g., "09:00-17:00"
                            # Convert time strings to datetime.time objects for comparison
                            start_time = datetime.datetime.strptime(start, "%H:%M").time()
                            end_time = datetime.datetime.strptime(end, "%H:%M").time()

                            # If activity has no time constraints, or its time is within person's availability
                            if (not activity.start_time and not activity.end_time) or \
                               (activity.start_time and activity.end_time and
                                datetime.datetime.strptime(activity.start_time, "%H:%M").time() >= start_time and
                                datetime.datetime.strptime(activity.end_time, "%H:%M").time() <= end_time):
                                available_people.append(person)
                                break # Person is available, no need to check other time ranges
                if available_people:
                    # Assign activity to a random available person.
                    assigned_person = random.choice(available_people)
                    shift = ["Morning", "Afternoon", "Evening"][activities.index(activity) % 3]
                    self.schedule[date_str][shift].append({"activity": activity, "person": assigned_person})
    def display_schedule(self) -> None:
        """
        Displays the generated schedule in a human-readable format.
        """
        if not self.schedule:
            print("No schedule has been generated yet.")
            return

        for date_str, shifts in self.schedule.items():
            print(f"\nDate: {date_str}")
            for shift, assignments in shifts.items():
                print(f"  {shift}:")
                if not assignments:
                    print("    No activities scheduled.")
                else:
                    for assignment in assignments:
                        activity = assignment["activity"]
                        person = assignment["person"]
                        print(f"    - {activity} assigned to {person}")

# =============================================================================
# 3. Input Modules (Extendable)
# =============================================================================

class DataManager:
    """
    Manages the loading and saving of data (entities) to/from a JSON file.
    Supports basic data validation.
    """
    def __init__(self, filename: str = "data.json"):
        """
        Initialize the DataManager.

        Args:
            filename (str, optional): The name of the JSON file to use for persistence.
                Defaults to "data.json".
        """
        self.filename = filename
        self.data = {"Person": [], "Department": [], "Activity": []}  # Store data in memory

    def load_data(self) -> None:
        """
        Loads data from the JSON file.  Handles file not found and JSON decode errors.
        """
        if not os.path.exists(self.filename):
            print(f"Info: Data file '{self.filename}' not found.  Starting with empty data.")
            return  # No file, start with empty data

        try:
            with open(self.filename, "r") as f:
                self.data = json.load(f)  # Load the entire structure
                # Convert loaded data into Entity objects.
                self.data["Person"] = [Person(**p) for p in self.data["Person"]]
                self.data["Department"] = [Department(**d) for d in self.data["Department"]]
                self.data["Activity"] = [Activity(**a) for a in self.data["Activity"]]
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in data file '{self.filename}'.  Starting with empty data.")
            self.data = {"Person": [], "Department": [], "Activity": []}  # Ensure data is initialized
        except Exception as e:
            print(f"An unexpected error occurred while loading data: {e}")
            self.data = {"Person": [], "Department": [], "Activity": []}

    def save_data(self) -> None:
        """
        Saves data to the JSON file.  Handles file writing errors.
        """
        try:
            # Convert Entity objects back to dictionaries for JSON serialization.  Use a helper.
            serializable_data = {
                "Person": [self._serialize_entity(p) for p in self.data["Person"]],
                "Department": [self._serialize_entity(d) for d in self.data["Department"]],
                "Activity": [self._serialize_entity(a) for a in self.data["Activity"]]
            }
            with open(self.filename, "w") as f:
                json.dump(serializable_data, f, indent=4)
            print(f"Data saved successfully to '{self.filename}'.")
        except Exception as e:
            print(f"Error saving data to '{self.filename}': {e}")

    def _serialize_entity(self, entity: Entity) -> Dict[str, Any]:
        """
        Helper method to convert an Entity object into a dictionary suitable for JSON serialization.
        This handles the different attributes of each entity type.

        Args:
            entity (Entity): The Entity object to serialize.

        Returns:
            Dict[str, Any]: A dictionary representation of the entity.
        """
        if isinstance(entity, Person):
            return {
                "name": entity.name,
                "skills": entity.skills,
                "availability": entity.availability,
                "preferences": entity.preferences,
            }
        elif isinstance(entity, Department):
            return {
                "name": entity.name,
                "people": [p.id for p in entity.people],  # Store IDs, not full Person objects
            }
        elif isinstance(entity, Activity):
            return {
                "name": entity.name,
                "required_skills": entity.required_skills,
                "duration": entity.duration,
                "start_time": entity.start_time,
                "end_time": entity.end_time,
                "location": entity.location,
            }
        else:
            raise TypeError(f"Cannot serialize entity of type {type(entity)}")

    def add_entity(self, entity: Entity) -> None:
        """
        Adds an entity to the data manager.

        Args:
            entity (Entity): The entity to add.
        """
        entity_type = entity.entity_type
        if entity_type in self.data:
            # Check for duplicates
            if any(e.name == entity.name for e in self.data[entity_type]):
                print(f"Error: An entity with the name '{entity.name}' already exists for type '{entity_type}'.")
                return
            self.data[entity_type].append(entity)
            print(f"Added {entity} to {entity_type}s.")
        else:
            print(f"Error: Invalid entity type '{entity_type}'.")

    def get_entities(self, entity_type: str) -> List[Entity]:
        """
        Retrieves entities of a specific type.

        Args:
            entity_type (str): The type of entities to retrieve (e.g., "Person", "Activity").

        Returns:
            List[Entity]: A list of entities of the specified type.  Returns an empty list if the
            entity type is invalid or no entities of that type exist.
        """
        if entity_type in self.data:
            return self.data[entity_type]
        else:
            print(f"Warning: No entities found for type '{entity_type}'.")
            return []

    def update_entity(self, entity_type: str, entity_id: int, **kwargs: Any) -> None:
        """
        Updates an existing entity with new attributes.

        Args:
            entity_type (str): The type of the entity to update (e.g., "Person").
            entity_id (int): The ID of the entity to update.
            **kwargs:  Keyword arguments representing the attributes to update
                (e.g., name="New Name", skills=["NewSkill1", "NewSkill2"]).
        """
        entities = self.get_entities(entity_type)
        for entity in entities:
            if entity.id == entity_id:
                for key, value in kwargs.items():
                    if hasattr(entity, key):
                        setattr(entity, key, value)
                        print(f"Updated {key} for {entity} to {value}.")
                    else:
                        print(f"Warning: Entity {entity} has no attribute '{key}'.")
                return
        print(f"Error: No {entity_type} found with ID {entity_id}.")

    def delete_entity(self, entity_type: str, entity_id: int) -> None:
        """
        Deletes an entity.

        Args:
            entity_type (str): The type of the entity to delete.
            entity_id (int): The ID of the entity to delete.
        """
        entities = self.get_entities(entity_type)
        for entity in entities:
            if entity.id == entity_id:
                self.data[entity_type].remove(entity)
                print(f"Deleted {entity} from {entity_type}s.")
                return
        print(f"Error: No {entity_type} found with ID {entity_id}.")

    def add_person_to_department(self, person_id: int, department_id: int) -> None:
        """Adds a person to a department.

        Args:
            person_id (int): The ID of the person to add.
            department_id (int): The ID of the department to add the person to.
        """
        person = None
        department = None

        for p in self.data["Person"]:
            if p.id == person_id:
                person = p
                break

        for d in self.data["Department"]:
            if d.id == department_id:
                department = d
                break
        if person and department:
            if person not in department.people:
                department.people.append(person)
                print(f"Added {person.name} to Department: {department.name}")
            else:
                print(f"{person.name} is already in Department: {department.name}")
        else:
            if not person:
                print(f"Person with id {person_id} not found")
            if not department:
                print(f"Department with id {department_id} not found.")

# =============================================================================
# 4. Input Modules (Extendable)
# =============================================================================
class InputModule:
    """
    Base class for input modules.  Provides a common interface for
    interacting with the data and getting user input.
    """
    def __init__(self, data_manager: DataManager):
        """
        Initialize the InputModule.

        Args:
            data_manager (DataManager): The DataManager instance to use.
        """
        self.data_manager = data_manager

    def get_user_input(self, prompt: str) -> str:
        """
        Gets user input from the console.  This is a basic implementation.
        Consider using a library like prompt_toolkit or inquirer for more
        advanced input handling (e.g., autocompletion, validation).

        Args:
            prompt (str): The prompt to display to the user.

        Returns:
            str: The user's input.
        """
        return input(prompt)

    def display_message(self, message: str) -> None:
        """
        Displays a message to the user.  This is a basic implementation.
        Consider using a library like rich for styled output.

        Args:
            message (str): The message to display.
        """
        print(message)

    def get_int_input(self, prompt: str) -> int:
        """Gets an integer from user input."""
        while True:
            try:
                user_input = self.get_user_input(prompt)
                return int(user_input)
            except ValueError:
                self.display_message("Invalid input. Please enter an integer.")

    def get_date_input(self, prompt: str) -> datetime.date:
        """Gets a date from user input."""
        while True:
            date_str = self.get_user_input(prompt)
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                self.display_message("Invalid date format. Please use YYYY-MM-DD.")

class CLIMenu(InputModule):
    """
    Provides a command-line menu for interacting with the application.
    """
    def __init__(self, data_manager: DataManager):
        super().__init__(data_manager)

    def display_main_menu(self):
        """Displays the main menu."""
        print("\n--- Dynamic Routine/Roster Manager ---")
        print("1. Manage Persons")
        print("2. Manage Departments")
        print("3. Manage Activities")
        print("4. Generate Schedule")
        print("5. Display Data")
        print("6. Save Data")
        print("7. Load Data")
        print("0. Exit")

    def display_person_menu(self):
        """Displays the person management menu."""
        print("\n--- Person Management Menu ---")
        print("1. Add Person")
        print("2. View Persons")
        print("3. Update Person")
        print("4. Delete Person")
        print("0. Back to Main Menu")

    def display_department_menu(self):
        """Displays the department management menu."""
        print("\n--- Department Management Menu ---")
        print("1. Add Department")
        print("2. View Departments")
        print("3. Update Department")
        print("4. Delete Department")
        print("5. Add Person to Department")
        print("0. Back to Main Menu")

    def display_activity_menu(self):
        """Displays the activity management menu."""
        print("\n--- Activity Management Menu ---")
        print("1. Add Activity")
        print("2. View Activities")
        print("3. Update Activity")
        print("4. Delete Activity")
        print("0. Back to Main Menu")

    def run(self):
        """Runs the main menu loop."""
        while True:
            self.display_main_menu()
            choice = self.get_int_input("Enter your choice: ")

            if choice == 1:
                self.run_person_menu()
            elif choice == 2:
                self.run_department_menu()
            elif choice == 3:
                self.run_activity_menu()
            elif choice == 4:
                self.run_schedule_generation()
            elif choice == 5:
                self.display_all_data()
            elif choice == 6:
                self.data_manager.save_data()
            elif choice == 7:
                self.data_manager.load_data()
            elif choice == 0:
                print("Exiting application.")
                break
            else:
                print("Invalid choice. Please try again.")

    def run_person_menu(self):
        """Runs the person management menu loop."""
        while True:
            self.display_person_menu()
            choice = self.get_int_input("Enter your choice: ")

            if choice == 1:
                self.add_person()
            elif choice == 2:
                self.view_persons()
            elif choice == 3:
                self.update_person()
            elif choice == 4:
                self.delete_person()
            elif choice == 0:
                break
            else:
                print("Invalid choice. Please try again.")

    def run_department_menu(self):
        """Runs the department management menu loop."""
        while True:
            self.display_department_menu()
            choice = self.get_int_input("Enter your choice: ")

            if choice == 1:
                self.add_department()
            elif choice == 2:
                self.view_departments()
            elif choice == 3:
                self.update_department()
            elif choice == 4:
                self.delete_department()
            elif choice == 5:
                self.add_person_to_department()
            elif choice == 0:
                break
            else:
                print("Invalid choice. Please try again.")

    def run_activity_menu(self):
        """Runs the activity management menu loop."""
        while True:
            self.display_activity_menu()
            choice = self.get_int_input("Enter your choice: ")

            if choice == 1:
                self.add_activity()
            elif choice == 2:
                self.view_activities()
            elif choice == 3:
                self.update_activity()
            elif choice == 4:
                self.delete_activity()
            elif choice == 0:
                break
            else:
                print("Invalid choice. Please try again.")

    def add_person(self):
        """Adds a new person."""
        name = self.get_user_input("Enter person's name: ")
        skills = self.get_user_input("Enter person's skills (comma-separated): ").split(",")
        availability = self.get_user_input("Enter person's availability (e.g., Monday:09:00-17:00,Tuesday:10:00-18:00): ")
        # Convert availability string to a dictionary
        availability_dict = {}
        if availability: # Check if the user entered anything
            for item in availability.split(","):
                parts = item.split(":")
                if len(parts) == 2:
                  day, times = parts
                  availability_dict[day] = times.split(" ")
                else:
                    print(f"Skipping invalid availability entry: {item}")

        preferences = self.get_user_input("Enter person's preferences (e.g., Task1:5,Task2:3): ")
        # Convert preferences string to a dictionary
        preferences_dict = {}
        if preferences:
            for item in preferences.split(","):
                parts = item.split(":")
                if len(parts) == 2:
                    task, preference = parts
                    preferences_dict[task] = int(preference)
                else:
                    print(f"Skipping invalid preference entry: {item}")

        person = Person(name, skills, availability_dict, preferences_dict)
        self.data_manager.add_entity(person)

    def view_persons(self):
        """Displays all persons."""
        persons = self.data_manager.get_entities("Person")
        if not persons:
            print("No persons found.")
            return
        print("\n--- Persons ---")
        for person in persons:
            print(person)

    def update_person(self):
        """Updates an existing person."""
        self.view_persons()
        person_id = self.get_int_input("Enter the ID of the person to update: ")
        name = self.get_user_input("Enter new name (leave blank to keep current): ")
        skills = self.get_user_input("Enter new skills (comma-separated, leave blank to keep current): ")
        availability = self.get_user_input("Enter new availability (e.g., Monday:09:00-17:00,Tuesday:10:00-18:00, leave blank to keep current): ")
        preferences = self.get_user_input("Enter new preferences (e.g., Task1:5,Task2:3, leave blank to keep current): ")

        # Convert availability string to a dictionary
        availability_dict = {}
        if availability: # Check if the user entered anything
            for item in availability.split(","):
                parts = item.split(":")
                if len(parts) == 2:
                  day, times = parts
                  availability_dict[day] = times.split(" ")
                else:
                    print(f"Skipping invalid availability entry: {item}")

        # Convert preferences string to a dictionary
        preferences_dict = {}
        if preferences:
            for item in preferences.split(","):
                parts = item.split(":")
                if len(parts) == 2:
                    task, preference = parts
                    preferences_dict[task] = int(preference)
                else:
                    print(f"Skipping invalid preference entry: {item}")
        update_data = {}
        if name:
            update_data["name"] = name
        if skills:
            update_data["skills"] = skills.split(",")
        if availability:
            update_data["availability"] = availability_dict
        if preferences:
            update_data["preferences"] = preferences_dict
        self.data_manager.update_entity("Person", person_id, **update_data)

    def delete_person(self):
        """Deletes a person."""
        self.view_persons()
        person_id = self.get_int_input("Enter the ID of the person to delete: ")
        self.data_manager.delete_entity("Person", person_id)

    def add_department(self):
        """Adds a new department."""
        name = self.get_user_input("Enter department name: ")
        department = Department(name)
        self.data_manager.add_entity(department)

    def view_departments(self):
        """Displays all departments."""
        departments = self.data_manager.get_entities("Department")
        if not departments:
            print("No departments found.")
            return
        print("\n--- Departments ---")
        for department in departments:
            print(department)

    def update_department(self):
        """Updates an existing department."""
        self.view_departments()
        department_id = self.get_int_input("Enter the ID of the department to update: ")
        name = self.get_user_input("Enter new name (leave blank to keep current): ")
        if name:
            self.data_manager.update_entity("Department", department_id, name=name)

    def delete_department(self):
        """Deletes a department."""
        self.view_departments()
        department_id = self.get_int_input("Enter the ID of the department to delete: ")
        self.data_manager.delete_entity("Department", department_id)

    def add_person_to_department(self):
        """Adds a person to a department"""
        self.view_persons()
        person_id = self.get_int_input("Enter the ID of the person to add to a department: ")
        self.view_departments()
        department_id = self.get_int_input("Enter the ID of the department to add the person to: ")
        self.data_manager.add_person_to_department(person_id, department_id)

    def add_activity(self):
        """Adds a new activity."""
        name = self.get_user_input("Enter activity name: ")
        required_skills = self.get_user_input("Enter required skills (comma-separated): ").split(",")
        duration = self.get_int_input("Enter duration in hours: ")
        start_time = self.get_user_input("Enter start time (HH:MM, leave blank for any): ")
        end_time = self.get_user_input("Enter end time (HH:MM, leave blank for any): ")
        location = self.get_user_input("Enter location (leave blank for any): ")

        activity = Activity(name, required_skills, duration, start_time, end_time, location)
        self.data_manager.add_entity(activity)

    def view_activities(self):
        """Displays all activities."""
        activities = self.data_manager.get_entities("Activity")
        if not activities:
            print("No activities found.")
            return
        print("\n--- Activities ---")
        for activity in activities:
            print(activity)

    def update_activity(self):
        """Updates an existing activity."""
        self.view_activities()
        activity_id = self.get_int_input("Enter the ID of the activity to update: ")
        name = self.get_user_input("Enter new name (leave blank to keep current): ")
        required_skills = self.get_user_input("Enter new required skills (comma-separated, leave blank to keep current): ")
        duration = self.get_int_input("Enter new duration in hours (leave blank to keep current): ")
        start_time = self.get_user_input("Enter new start time (HH:MM, leave blank to keep current): ")
        end_time = self.get_user_input("Enter new end time (HH:MM, leave blank to keep current): ")
        location = self.get_user_input("Enter new location (leave blank to keep current): ")

        update_data = {}
        if name:
            update_data["name"] = name
        if required_skills:
            update_data["required_skills"] = required_skills.split(",")
        if duration:
            update_data["duration"] = duration
        if start_time:
            update_data["start_time"] = start_time
        if end_time:
            update_data["end_time"] = end_time
        if location:
            update_data["location"] = location
        self.data_manager.update_entity("Activity", activity_id, **update_data)

    def delete_activity(self):
        """Deletes an activity."""
        self.view_activities()
        activity_id = self.get_int_input("Enter the ID of the activity to delete: ")
        self.data_manager.delete_entity("Activity", activity_id)

    def display_all_data(self):
        """Displays all data."""
        print("\n--- All Data ---")
        print("\nPersons:")
        self.view_persons()  # Reuse view methods for consistent output
        print("\nDepartments:")
        self.view_departments()
        print("\nActivities:")
        self.view_activities()

    def run_schedule_generation(self):
        """Runs the schedule generation process."""
        year = self.get_int_input("Enter the year for the schedule: ")
        month = self.get_int_input("Enter the month for the schedule (1-12): ")
        algorithm = self.get_user_input("Enter scheduling algorithm ('round_robin' or 'availability_match'): ")
        generator = ScheduleGenerator(self.data_manager.data) # Pass the data, not the manager
        schedule = generator.generate_monthly_schedule(year, month, algorithm)
        if schedule:
            generator.display_schedule()
        else:
            print("Failed to generate schedule.")
def main():
    """Main function to run the application."""
    data_manager = DataManager()
    data_manager.load_data()  # Load data at startup
    cli_menu = CLIMenu(data_manager)
    cli_menu.run()  # Start the CLI menu
    data_manager.save_data() # Save data before exit

if __name__ == "__main__":
    main()