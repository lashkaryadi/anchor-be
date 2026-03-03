"""Seed the database with data matching the frontend mock data exactly."""

from sqlalchemy.orm import Session
from app.models.employee import Employee, RiskFactor, EngagementScore
from app.models.team import Team
from app.models.intervention import Intervention
from app.models.analytics import RetentionTrend, TurnoverCost, DepartmentRiskDistribution
from app.models.career import CareerPath, CareerSkill, InternalOpportunity


def seed_all(db: Session):
    if db.query(Employee).count() > 0:
        return  # already seeded

    _seed_employees(db)
    _seed_teams(db)
    _seed_interventions(db)
    _seed_retention_trends(db)
    _seed_turnover_costs(db)
    _seed_risk_distributions(db)
    _seed_careers(db)
    db.commit()


def _seed_employees(db: Session):
    employees_data = [
        {
            "id": "1", "name": "Sarah Chen", "role": "Senior Engineer", "department": "Engineering",
            "avatar": "SC", "risk_score": 87, "risk_level": "critical", "confidence": 92,
            "tenure": "3.2 yrs", "last_engagement": "2 days ago",
            "salary": 145000, "market_rate": 172000, "manager_score": 6.2,
            "last_promotion": "18 months ago",
            "recent_changes": ["Declined team offsite", "Updated LinkedIn", "Reduced Slack activity"],
            "factors": [
                {"label": "Compensation below market", "impact": 34, "direction": "up"},
                {"label": "No promotion in 18 months", "impact": 28, "direction": "up"},
                {"label": "Decreased PR activity", "impact": 22, "direction": "up"},
                {"label": "Manager relationship", "impact": 16, "direction": "down"},
            ],
            "engagement": [82, 78, 72, 65, 58, 52, 48],
        },
        {
            "id": "2", "name": "Marcus Johnson", "role": "Product Manager", "department": "Product",
            "avatar": "MJ", "risk_score": 73, "risk_level": "high", "confidence": 85,
            "tenure": "2.1 yrs", "last_engagement": "1 week ago",
            "salary": 135000, "market_rate": 148000, "manager_score": 7.1,
            "last_promotion": "14 months ago",
            "recent_changes": ["Skipped last 2 all-hands", "Reduced meeting participation"],
            "factors": [
                {"label": "Team restructuring impact", "impact": 38, "direction": "up"},
                {"label": "Career growth stagnation", "impact": 30, "direction": "up"},
                {"label": "Engagement score decline", "impact": 20, "direction": "up"},
                {"label": "Strong peer relationships", "impact": 12, "direction": "down"},
            ],
            "engagement": [90, 85, 80, 74, 68, 64, 60],
        },
        {
            "id": "3", "name": "Emily Rodriguez", "role": "Design Lead", "department": "Design",
            "avatar": "ER", "risk_score": 62, "risk_level": "medium", "confidence": 78,
            "tenure": "4.5 yrs", "last_engagement": "3 days ago",
            "salary": 128000, "market_rate": 135000, "manager_score": 8.4,
            "last_promotion": "8 months ago",
            "recent_changes": ["Requested role clarity meeting"],
            "factors": [
                {"label": "Limited advancement path", "impact": 35, "direction": "up"},
                {"label": "Workload concerns", "impact": 25, "direction": "up"},
                {"label": "Strong company alignment", "impact": 20, "direction": "down"},
                {"label": "Recent recognition", "impact": 20, "direction": "down"},
            ],
            "engagement": [88, 85, 82, 78, 75, 70, 68],
        },
        {
            "id": "4", "name": "James Park", "role": "Data Scientist", "department": "Engineering",
            "avatar": "JP", "risk_score": 45, "risk_level": "medium", "confidence": 72,
            "tenure": "1.8 yrs", "last_engagement": "1 day ago",
            "salary": 155000, "market_rate": 165000, "manager_score": 8.8,
            "last_promotion": "6 months ago",
            "recent_changes": [],
            "factors": [
                {"label": "Competitive offers likely", "impact": 30, "direction": "up"},
                {"label": "Strong project engagement", "impact": 30, "direction": "down"},
                {"label": "Good manager relationship", "impact": 25, "direction": "down"},
                {"label": "Commute concerns", "impact": 15, "direction": "up"},
            ],
            "engagement": [75, 78, 80, 77, 74, 72, 70],
        },
        {
            "id": "5", "name": "Aisha Patel", "role": "Marketing Director", "department": "Marketing",
            "avatar": "AP", "risk_score": 28, "risk_level": "low", "confidence": 88,
            "tenure": "5.3 yrs", "last_engagement": "Today",
            "salary": 168000, "market_rate": 162000, "manager_score": 9.1,
            "last_promotion": "3 months ago",
            "recent_changes": ["Volunteered for mentorship program"],
            "factors": [
                {"label": "Strong leadership role", "impact": 35, "direction": "down"},
                {"label": "Recent promotion", "impact": 30, "direction": "down"},
                {"label": "High compensation", "impact": 25, "direction": "down"},
                {"label": "Industry networking", "impact": 10, "direction": "up"},
            ],
            "engagement": [85, 87, 88, 90, 91, 92, 93],
        },
        {
            "id": "6", "name": "David Kim", "role": "VP of Sales", "department": "Sales",
            "avatar": "DK", "risk_score": 15, "risk_level": "low", "confidence": 94,
            "tenure": "6.1 yrs", "last_engagement": "Today",
            "salary": 210000, "market_rate": 195000, "manager_score": 9.5,
            "last_promotion": "5 months ago",
            "recent_changes": [],
            "factors": [
                {"label": "Executive track", "impact": 40, "direction": "down"},
                {"label": "Equity vesting", "impact": 30, "direction": "down"},
                {"label": "Team loyalty", "impact": 20, "direction": "down"},
                {"label": "Market demand", "impact": 10, "direction": "up"},
            ],
            "engagement": [90, 91, 92, 93, 94, 94, 95],
        },
    ]

    for data in employees_data:
        factors = data.pop("factors")
        engagement = data.pop("engagement")

        emp = Employee(**data)
        db.add(emp)
        db.flush()

        for f in factors:
            db.add(RiskFactor(employee_id=emp.id, **f))

        for i, score in enumerate(engagement):
            db.add(EngagementScore(employee_id=emp.id, period=i, score=score))


def _seed_teams(db: Session):
    teams = [
        Team(name="Engineering", headcount=48, avg_risk=52, high_risk_count=8, turnover_rate=14.2, trend="up"),
        Team(name="Product", headcount=22, avg_risk=44, high_risk_count=4, turnover_rate=11.5, trend="up"),
        Team(name="Design", headcount=15, avg_risk=38, high_risk_count=2, turnover_rate=8.3, trend="stable"),
        Team(name="Marketing", headcount=28, avg_risk=25, high_risk_count=1, turnover_rate=6.1, trend="down"),
        Team(name="Sales", headcount=35, avg_risk=31, high_risk_count=3, turnover_rate=9.8, trend="stable"),
        Team(name="Operations", headcount=18, avg_risk=22, high_risk_count=0, turnover_rate=4.2, trend="down"),
    ]
    db.add_all(teams)


def _seed_interventions(db: Session):
    interventions = [
        Intervention(id="1", employee_name="Sarah Chen", type="Compensation Review", status="pending", priority="critical", assigned_to="VP Engineering", created_at="2026-02-28", due_date="2026-03-07"),
        Intervention(id="2", employee_name="Sarah Chen", type="Career Path Discussion", status="in_progress", priority="critical", assigned_to="Engineering Manager", created_at="2026-02-25", due_date="2026-03-05"),
        Intervention(id="3", employee_name="Marcus Johnson", type="Stay Interview", status="pending", priority="high", assigned_to="Product Director", created_at="2026-03-01", due_date="2026-03-10"),
        Intervention(id="4", employee_name="Emily Rodriguez", type="Role Expansion", status="in_progress", priority="medium", assigned_to="Design Director", created_at="2026-02-20", due_date="2026-03-15", effectiveness=45),
        Intervention(id="5", employee_name="James Park", type="Mentorship Pairing", status="completed", priority="medium", assigned_to="Data Lead", created_at="2026-02-10", due_date="2026-02-28", effectiveness=72),
        Intervention(id="6", employee_name="Alex Turner", type="Flexible Work Arrangement", status="completed", priority="high", assigned_to="HR Manager", created_at="2026-01-15", due_date="2026-02-01", effectiveness=88),
    ]
    db.add_all(interventions)


def _seed_retention_trends(db: Session):
    data = [
        RetentionTrend(month="Sep", retained=96.2, target=95, at_risk=12),
        RetentionTrend(month="Oct", retained=95.8, target=95, at_risk=15),
        RetentionTrend(month="Nov", retained=94.5, target=95, at_risk=18),
        RetentionTrend(month="Dec", retained=93.1, target=95, at_risk=22),
        RetentionTrend(month="Jan", retained=94.2, target=95, at_risk=19),
        RetentionTrend(month="Feb", retained=94.8, target=95, at_risk=17),
    ]
    db.add_all(data)


def _seed_turnover_costs(db: Session):
    data = [
        TurnoverCost(month="Sep", actual=45000, prevented=120000),
        TurnoverCost(month="Oct", actual=68000, prevented=95000),
        TurnoverCost(month="Nov", actual=92000, prevented=180000),
        TurnoverCost(month="Dec", actual=55000, prevented=210000),
        TurnoverCost(month="Jan", actual=38000, prevented=155000),
        TurnoverCost(month="Feb", actual=42000, prevented=190000),
    ]
    db.add_all(data)


def _seed_risk_distributions(db: Session):
    data = [
        DepartmentRiskDistribution(department="Engineering", critical=3, high=5, medium=12, low=28),
        DepartmentRiskDistribution(department="Product", critical=1, high=3, medium=6, low=12),
        DepartmentRiskDistribution(department="Design", critical=0, high=2, medium=4, low=9),
        DepartmentRiskDistribution(department="Marketing", critical=0, high=1, medium=5, low=22),
        DepartmentRiskDistribution(department="Sales", critical=1, high=2, medium=8, low=24),
        DepartmentRiskDistribution(department="Operations", critical=0, high=0, medium=3, low=15),
    ]
    db.add_all(data)


def _seed_careers(db: Session):
    paths = [
        {
            "employee_name": "Sarah Chen", "avatar": "SC",
            "current_role": "Senior Engineer", "next_role": "Staff Engineer",
            "readiness": 72, "timeline": "6-9 months",
            "skills": [
                {"name": "System Design", "level": 85},
                {"name": "Leadership", "level": 60},
                {"name": "Mentorship", "level": 55},
                {"name": "Architecture", "level": 78},
            ],
        },
        {
            "employee_name": "Marcus Johnson", "avatar": "MJ",
            "current_role": "Product Manager", "next_role": "Senior PM",
            "readiness": 58, "timeline": "9-12 months",
            "skills": [
                {"name": "Strategy", "level": 70},
                {"name": "Data Analysis", "level": 65},
                {"name": "Stakeholder Mgmt", "level": 80},
                {"name": "Technical Depth", "level": 45},
            ],
        },
        {
            "employee_name": "Emily Rodriguez", "avatar": "ER",
            "current_role": "Design Lead", "next_role": "Head of Design",
            "readiness": 82, "timeline": "3-6 months",
            "skills": [
                {"name": "Design Systems", "level": 92},
                {"name": "Team Management", "level": 75},
                {"name": "Business Acumen", "level": 68},
                {"name": "UX Research", "level": 88},
            ],
        },
    ]

    for p in paths:
        skills_data = p.pop("skills")
        cp = CareerPath(**p)
        db.add(cp)
        db.flush()
        for s in skills_data:
            db.add(CareerSkill(career_path_id=cp.id, **s))

    opportunities = [
        InternalOpportunity(title="Engineering Manager", department="Engineering", open_since="2 weeks", matches=3),
        InternalOpportunity(title="Principal Designer", department="Design", open_since="1 month", matches=1),
        InternalOpportunity(title="VP Product", department="Product", open_since="3 weeks", matches=2),
    ]
    db.add_all(opportunities)
