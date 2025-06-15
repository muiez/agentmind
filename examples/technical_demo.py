"""
Technical Demo: Building a Smart Sales Bot with AgentMind

This demo shows how to build a sales bot that remembers every interaction,
tracks deal progress, and provides intelligent follow-ups.
"""
import json
from datetime import datetime, timedelta
from agentmind import Memory, RecallStrategy

# Initialize memory with business configuration
memory = Memory(
    api_key="demo_key",
    local_mode=True,  # Use hosted mode in production
    config={
        "namespace": "sales_bot",
        "retention_days": 365,  # Keep sales data for a year
        "auto_summarize": True
    }
)


class SalesBot:
    """AI Sales Assistant powered by AgentMind"""
    
    def __init__(self, memory: Memory):
        self.memory = memory
    
    def handle_new_lead(self, lead_info):
        """Process a new lead"""
        print(f"\n🎯 New Lead: {lead_info['name']} from {lead_info['company']}")
        
        # Store comprehensive lead information
        self.memory.remember(
            f"New lead: {lead_info['name']} from {lead_info['company']}",
            metadata={
                "type": "lead",
                "stage": "initial_contact",
                "company": lead_info['company'],
                "contact": lead_info['name'],
                "email": lead_info['email'],
                "importance": 0.8
            }
        )
        
        # Store specific interests
        if 'interests' in lead_info:
            for interest in lead_info['interests']:
                self.memory.remember(
                    f"{lead_info['name']} interested in {interest}",
                    metadata={
                        "type": "interest",
                        "contact": lead_info['name'],
                        "topic": interest
                    }
                )
        
        return f"Hi {lead_info['name']}! I see you're interested in our {', '.join(lead_info['interests'])}. Let me tell you more..."
    
    def handle_follow_up(self, contact_name):
        """Intelligent follow-up based on history"""
        print(f"\n📞 Following up with {contact_name}")
        
        # Recall all context about this contact
        context = self.memory.recall(
            f"{contact_name} history interests stage",
            strategy=RecallStrategy.HYBRID,
            limit=10
        )
        
        # Get specific facts
        facts = self.memory.get_facts(category="interest")
        stage_info = [f for f in facts if f.get('contact') == contact_name]
        
        # Generate personalized follow-up
        if context:
            print("📋 Retrieved context:")
            for item in context[:3]:
                print(f"  - {item}")
            
            return self._generate_follow_up(contact_name, context)
        else:
            return f"Hi {contact_name}, I'd love to learn more about your needs."
    
    def track_interaction(self, contact_name, interaction_type, notes):
        """Track every interaction"""
        self.memory.remember(
            f"{interaction_type} with {contact_name}: {notes}",
            metadata={
                "type": "interaction",
                "contact": contact_name,
                "interaction_type": interaction_type,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        # Update deal stage if mentioned
        if "interested" in notes.lower():
            self._update_stage(contact_name, "qualified")
        elif "demo" in notes.lower():
            self._update_stage(contact_name, "demo_scheduled")
        elif "pricing" in notes.lower():
            self._update_stage(contact_name, "negotiation")
    
    def get_pipeline_status(self):
        """Get current sales pipeline"""
        print("\n📊 Sales Pipeline Status")
        
        # In production, this would aggregate from the API
        all_memories = self.memory.get_facts()
        
        pipeline = {
            "initial_contact": 0,
            "qualified": 0,
            "demo_scheduled": 0,
            "negotiation": 0,
            "closed": 0
        }
        
        contacts = set()
        for memory in all_memories:
            if memory.get('type') == 'lead':
                stage = memory.get('stage', 'initial_contact')
                if stage in pipeline:
                    pipeline[stage] += 1
                contacts.add(memory.get('contact'))
        
        return {
            "total_contacts": len(contacts),
            "pipeline": pipeline,
            "conversion_rate": "23%"  # Would calculate from real data
        }
    
    def _generate_follow_up(self, contact_name, context):
        """Generate personalized follow-up message"""
        # Extract key information
        interests = [c for c in context if "interested in" in c]
        last_interaction = [c for c in context if "interaction" in c.lower()]
        
        message = f"Hi {contact_name}! "
        
        if last_interaction:
            message += "Following up on our last conversation. "
        
        if interests:
            interest = interests[0].split("interested in")[-1].strip()
            message += f"I have some updates on our {interest} solution that might interest you. "
        
        message += "Do you have 15 minutes this week to discuss?"
        
        return message
    
    def _update_stage(self, contact_name, new_stage):
        """Update deal stage"""
        self.memory.remember(
            f"{contact_name} moved to stage: {new_stage}",
            metadata={
                "type": "stage_change",
                "contact": contact_name,
                "stage": new_stage,
                "timestamp": datetime.now().isoformat()
            }
        )


def run_demo():
    """Run the technical demo"""
    print("🤖 AgentMind Technical Demo: Smart Sales Bot")
    print("=" * 50)
    
    bot = SalesBot(memory)
    
    # Day 1: New leads come in
    print("\n--- Day 1: New Leads ---")
    
    lead1 = {
        "name": "Alice Johnson",
        "company": "TechCorp",
        "email": "alice@techcorp.com",
        "interests": ["API integration", "enterprise plan"]
    }
    
    response = bot.handle_new_lead(lead1)
    print(f"🤖 Bot: {response}")
    
    lead2 = {
        "name": "Bob Smith",
        "company": "StartupXYZ",
        "email": "bob@startupxyz.com",
        "interests": ["memory optimization", "Python SDK"]
    }
    
    response = bot.handle_new_lead(lead2)
    print(f"🤖 Bot: {response}")
    
    # Day 2: Follow up
    print("\n--- Day 2: Intelligent Follow-ups ---")
    
    response = bot.handle_follow_up("Alice Johnson")
    print(f"🤖 Bot: {response}")
    
    # Track interactions
    print("\n--- Tracking Interactions ---")
    
    bot.track_interaction(
        "Alice Johnson",
        "phone_call",
        "Very interested in enterprise features, wants a demo next week"
    )
    print("✓ Interaction tracked")
    
    bot.track_interaction(
        "Bob Smith",
        "email",
        "Asking about pricing for 10 developer seats"
    )
    print("✓ Interaction tracked")
    
    # Day 7: Check pipeline
    print("\n--- Day 7: Pipeline Analysis ---")
    
    pipeline = bot.get_pipeline_status()
    print(json.dumps(pipeline, indent=2))
    
    # Show the power of memory
    print("\n--- The Power of Memory ---")
    
    # Follow up with context
    response = bot.handle_follow_up("Alice Johnson")
    print(f"🤖 Bot: {response}")
    
    # Get full history
    print("\n📜 Alice's Complete History:")
    alice_history = memory.recall("Alice Johnson", limit=20)
    for idx, item in enumerate(alice_history, 1):
        print(f"{idx}. {item}")
    
    # Show memory stats
    print("\n--- Memory Statistics ---")
    stats = memory.get_stats()
    print(f"Total Memories: {stats.total_memories}")
    print(f"Categories: {[cat['name'] for cat in stats.popular_categories]}")
    
    print("\n✨ Benefits of AgentMind for Sales:")
    print("1. Never forget a lead detail")
    print("2. Automatic context for every interaction")
    print("3. Track deal progress intelligently")
    print("4. Personalized follow-ups that convert")
    print("5. Full audit trail for compliance")


if __name__ == "__main__":
    run_demo()
    
    print("\n\n🚀 Build YOUR smart sales bot with AgentMind")
    print("👉 pip install agentmind")
    print("👉 Full docs at docs.agentmind.ai")
    print("👉 Start free at agentmind.ai")