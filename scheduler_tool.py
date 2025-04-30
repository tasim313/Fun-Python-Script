import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import random
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import sqlite3
from collections import defaultdict

# Core Data Structures
@dataclass
class EntityDefinition:
    name: str
    fields: Dict[str, str]  # field_name: field_type

@dataclass
class EntityInstance:
    entity_type: str
    attributes: Dict[str, Any]
    id: str = field(default_factory=lambda: str(random.randint(1000, 9999)))

@dataclass
class ScheduleItem:
    date: str
    start_time: str
    end_time: str
    activity: str
    assigned_to: List[str]
    status: str = "scheduled"

@dataclass
class Constraint:
    name: str
    condition: str
    action: str

class ScheduleSystem:
    def __init__(self, persistence_type: str = 'json'):
        self.persistence_type = persistence_type
        self.entity_definitions: Dict[str, EntityDefinition] = {}
        self.entities: Dict[str, List[EntityInstance]] = defaultdict(list)
        self.schedules: Dict[str, List[ScheduleItem]] = defaultdict(list)
        self.constraints: List[Constraint] = []
        
        if persistence_type == 'sqlite':
            self.init_db()
        else:
            self.load_data()
    
    def init_db(self):
        self.conn = sqlite3.connect('schedule_system.db')
        self.create_tables()
        self.load_from_db()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create entity definitions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS entity_definitions (
            name TEXT PRIMARY KEY,
            fields_json TEXT
        )
        ''')
        
        # Create entities table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS entities (
            id TEXT PRIMARY KEY,
            entity_type TEXT,
            attributes_json TEXT
        )
        ''')
        
        # Create schedules table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            start_time TEXT,
            end_time TEXT,
            activity TEXT,
            assigned_to_json TEXT,
            status TEXT
        )
        ''')
        
        # Create constraints table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS constraints (
            name TEXT PRIMARY KEY,
            condition TEXT,
            action TEXT
        )
        ''')
        
        self.conn.commit()
    
    def load_from_db(self):
        cursor = self.conn.cursor()
        
        # Load entity definitions
        cursor.execute('SELECT name, fields_json FROM entity_definitions')
        for name, fields_json in cursor.fetchall():
            self.entity_definitions[name] = EntityDefinition(
                name=name,
                fields=json.loads(fields_json)
            )
        
        # Load entities
        cursor.execute('SELECT id, entity_type, attributes_json FROM entities')
        for id, entity_type, attributes_json in cursor.fetchall():
            self.entities[entity_type].append(
                EntityInstance(
                    entity_type=entity_type,
                    attributes=json.loads(attributes_json),
                    id=id
                )
            )
        
        # Load schedules
        cursor.execute('SELECT date, start_time, end_time, activity, assigned_to_json, status FROM schedules')
        for date, start_time, end_time, activity, assigned_to_json, status in cursor.fetchall():
            self.schedules[date].append(
                ScheduleItem(
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    activity=activity,
                    assigned_to=json.loads(assigned_to_json),
                    status=status
                )
            )
        
        # Load constraints
        cursor.execute('SELECT name, condition, action FROM constraints')
        for name, condition, action in cursor.fetchall():
            self.constraints.append(
                Constraint(
                    name=name,
                    condition=condition,
                    action=action
                )
            )
    
    def save_to_db(self):
        cursor = self.conn.cursor()
        
        # Clear tables
        cursor.execute('DELETE FROM entity_definitions')
        cursor.execute('DELETE FROM entities')
        cursor.execute('DELETE FROM schedules')
        cursor.execute('DELETE FROM constraints')
        
        # Save entity definitions
        for name, definition in self.entity_definitions.items():
            cursor.execute(
                'INSERT INTO entity_definitions (name, fields_json) VALUES (?, ?)',
                (name, json.dumps(definition.fields))
            )
        
        # Save entities
        for entity_type, instances in self.entities.items():
            for instance in instances:
                cursor.execute(
                    'INSERT INTO entities (id, entity_type, attributes_json) VALUES (?, ?, ?)',
                    (instance.id, entity_type, json.dumps(instance.attributes))
                )
        
        # Save schedules
        for date, items in self.schedules.items():
            for item in items:
                cursor.execute(
                    '''INSERT INTO schedules 
                    (date, start_time, end_time, activity, assigned_to_json, status)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                    (item.date, item.start_time, item.end_time, 
                     item.activity, json.dumps(item.assigned_to), item.status)
                )
        
        # Save constraints
        for constraint in self.constraints:
            cursor.execute(
                'INSERT INTO constraints (name, condition, action) VALUES (?, ?, ?)',
                (constraint.name, constraint.condition, constraint.action)
            )
        
        self.conn.commit()
    
    def load_data(self):
        if os.path.exists('entity_definitions.json'):
            with open('entity_definitions.json', 'r') as f:
                data = json.load(f)
                self.entity_definitions = {
                    name: EntityDefinition(name=name, fields=fields) 
                    for name, fields in data.items()
                }
        
        if os.path.exists('entities.json'):
            with open('entities.json', 'r') as f:
                data = json.load(f)
                self.entities = defaultdict(list)
                for entity_type, instances in data.items():
                    self.entities[entity_type] = [
                        EntityInstance(entity_type=entity_type, attributes=attrs)
                        for attrs in instances
                    ]
        
        if os.path.exists('schedules.json'):
            with open('schedules.json', 'r') as f:
                data = json.load(f)
                self.schedules = defaultdict(list)
                for date, items in data.items():
                    self.schedules[date] = [
                        ScheduleItem(**item) for item in items
                    ]
        
        if os.path.exists('constraints.json'):
            with open('constraints.json', 'r') as f:
                self.constraints = [
                    Constraint(**constraint) 
                    for constraint in json.load(f)
                ]
    
    def save_data(self):
        if self.persistence_type == 'sqlite':
            self.save_to_db()
        else:
            # Save entity definitions
            with open('entity_definitions.json', 'w') as f:
                json.dump(
                    {name: definition.fields 
                     for name, definition in self.entity_definitions.items()},
                    f
                )
            
            # Save entities
            with open('entities.json', 'w') as f:
                json.dump(
                    {entity_type: [instance.attributes 
                                  for instance in instances]
                     for entity_type, instances in self.entities.items()},
                    f
                )
            
            # Save schedules
            with open('schedules.json', 'w') as f:
                json.dump(
                    {date: [vars(item) for item in items]
                     for date, items in self.schedules.items()},
                    f
                )
            
            # Save constraints
            with open('constraints.json', 'w') as f:
                json.dump(
                    [vars(constraint) for constraint in self.constraints],
                    f
                )

    # Entity Management
    def define_entity(self, name: str, fields: Dict[str, str]):
        """Define a new entity type with custom fields"""
        self.entity_definitions[name] = EntityDefinition(name=name, fields=fields)
        self.save_data()
    
    def add_entity_instance(self, entity_type: str, attributes: Dict[str, Any]):
        """Add an instance of an entity type"""
        if entity_type not in self.entity_definitions:
            raise ValueError(f"Entity type {entity_type} not defined")
        
        # Validate fields
        definition = self.entity_definitions[entity_type]
        for field_name, field_type in definition.fields.items():
            if field_name not in attributes:
                raise ValueError(f"Missing required field: {field_name}")
            
            # Simple type checking
            if field_type == 'str' and not isinstance(attributes[field_name], str):
                raise ValueError(f"Field {field_name} should be str")
            elif field_type == 'int' and not isinstance(attributes[field_name], int):
                raise ValueError(f"Field {field_name} should be int")
            elif field_type == 'bool' and not isinstance(attributes[field_name], bool):
                raise ValueError(f"Field {field_name} should be bool")
        
        instance = EntityInstance(entity_type=entity_type, attributes=attributes)
        self.entities[entity_type].append(instance)
        self.save_data()
        return instance
    
    def get_entities(self, entity_type: str) -> List[EntityInstance]:
        """Get all instances of an entity type"""
        return self.entities.get(entity_type, [])
    
    # Schedule Generation
    def generate_monthly_schedule(self, year: int, month: int, 
                                activity_name: str, 
                                assignment_rule: str = 'round_robin'):
        """Generate a schedule for a month"""
        start_date = datetime(year, month, 1)
        end_date = (start_date + timedelta(days=32)).replace(day=1)
        
        current_date = start_date
        while current_date < end_date:
            self.generate_daily_schedule(current_date.strftime('%Y-%m-%d'), 
                                       activity_name, assignment_rule)
            current_date += timedelta(days=1)
        
        self.save_data()
    
    def generate_daily_schedule(self, date: str, activity_name: str, 
                              assignment_rule: str = 'round_robin'):
        """Generate schedule for a single day"""
        # Get available people for this date
        available_people = [
            p for p in self.get_entities('Person') 
            if self.is_available(p, date)
        ]
        
        if not available_people:
            print(f"No available people for {date}")
            return
        
        # Simple assignment rules
        if assignment_rule == 'round_robin':
            # Simple round robin assignment
            assigned = [available_people[0]]
        elif assignment_rule == 'random':
            assigned = [random.choice(available_people)]
        else:
            assigned = [available_people[0]]
        
        # Create schedule item
        schedule_item = ScheduleItem(
            date=date,
            start_time="09:00",
            end_time="17:00",
            activity=activity_name,
            assigned_to=[p.id for p in assigned]
        )
        
        self.schedules[date].append(schedule_item)
        self.save_data()
    
    def is_available(self, person: EntityInstance, date: str) -> bool:
        """Check if a person is available on a given date"""
        # Check if person has availability data
        if 'availability' in person.attributes:
            avail = person.attributes['availability']
            if isinstance(avail, dict) and date in avail:
                return avail[date]
        
        # Default to available if no specific data
        return True
    
    # Constraint Management
    def add_constraint(self, name: str, condition: str, action: str):
        """Add a scheduling constraint"""
        self.constraints.append(Constraint(name=name, condition=condition, action=action))
        self.save_data()
    
    def check_constraints(self, schedule_item: ScheduleItem) -> bool:
        """Check if a schedule item violates any constraints"""
        for constraint in self.constraints:
            # Simple condition checking - in a real system this would be more sophisticated
            if constraint.condition in str(schedule_item):
                print(f"Constraint violated: {constraint.name}")
                return False
        return True
    
    # Optimization Interface
    def optimize_schedule(self, algorithm: str = 'round_robin', 
                         objectives: List[str] = None):
        """Optimize the schedule using specified algorithm"""
        if objectives is None:
            objectives = ['fairness']
        
        if algorithm == 'round_robin':
            self.round_robin_optimization()
        elif algorithm == 'random':
            self.random_optimization()
        else:
            print(f"Algorithm {algorithm} not implemented")
    
    def round_robin_optimization(self):
        """Simple round-robin optimization"""
        people = self.get_entities('Person')
        if not people:
            return
        
        # Get all scheduled dates
        all_dates = sorted(self.schedules.keys())
        for i, date in enumerate(all_dates):
            # Skip if already assigned
            if any(item.assigned_to for item in self.schedules[date]):
                continue
            
            # Assign next person in round-robin
            person_idx = i % len(people)
            for item in self.schedules[date]:
                item.assigned_to = [people[person_idx].id]
        
        self.save_data()
    
    def random_optimization(self):
        """Random assignment optimization"""
        people = self.get_entities('Person')
        if not people:
            return
        
        for date, items in self.schedules.items():
            for item in items:
                if not item.assigned_to:
                    item.assigned_to = [random.choice(people).id]
        
        self.save_data()
    
    # Reporting
    def get_schedule_for_date(self, date: str) -> List[ScheduleItem]:
        """Get schedule for a specific date"""
        return self.schedules.get(date, [])
    
    def get_person_schedule(self, person_id: str) -> List[ScheduleItem]:
        """Get schedule for a specific person"""
        result = []
        for date, items in self.schedules.items():
            for item in items:
                if person_id in item.assigned_to:
                    result.append(item)
        return result
    
    def print_daily_schedule(self, date: str):
        """Print schedule for a day"""
        print(f"\nSchedule for {date}:")
        for item in self.get_schedule_for_date(date):
            people = ", ".join([
                self.get_person_name(pid) for pid in item.assigned_to
            ])
            print(f"{item.start_time}-{item.end_time}: {item.activity} (Assigned to: {people})")
    
    def get_person_name(self, person_id: str) -> str:
        """Get person name by ID"""
        for person in self.get_entities('Person'):
            if person.id == person_id:
                return person.attributes.get('name', 'Unknown')
        return "Unknown"

# Example Usage
def example_usage():
    system = ScheduleSystem(persistence_type='json')
    
    # Define entity types
    system.define_entity('Person', {
        'name': 'str',
        'skills': 'list',
        'availability': 'dict',
        'preferences': 'dict'
    })
    
    system.define_entity('Department', {
        'name': 'str',
        'location': 'str',
        'manager': 'str'
    })
    
    system.define_entity('Activity', {
        'name': 'str',
        'required_skills': 'list',
        'duration_hours': 'int'
    })
    
    # Add some people
    system.add_entity_instance('Person', {
        'name': 'Alice',
        'skills': ['nursing', 'first_aid'],
        'availability': {'2023-11-01': True, '2023-11-02': False},
        'preferences': {'shift': 'morning'}
    })
    
    system.add_entity_instance('Person', {
        'name': 'Bob',
        'skills': ['doctor', 'surgery'],
        'availability': {'2023-11-01': True, '2023-11-02': True},
        'preferences': {'shift': 'afternoon'}
    })
    
    # Add an activity
    system.add_entity_instance('Activity', {
        'name': 'Patient Rounds',
        'required_skills': ['nursing'],
        'duration_hours': 2
    })
    
    # Add a constraint
    system.add_constraint(
        name='no_double_shifts',
        condition='same_person_consecutive_days',
        action='reassign'
    )
    
    # Generate schedule for November 2023
    system.generate_monthly_schedule(2023, 11, 'Patient Rounds')
    
    # Optimize
    system.optimize_schedule(algorithm='round_robin')
    
    # Print schedule
    system.print_daily_schedule('2023-11-01')
    system.print_daily_schedule('2023-11-02')

if __name__ == '__main__':
    example_usage()