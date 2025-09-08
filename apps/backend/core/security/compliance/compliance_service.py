"""Security compliance and reporting framework for ZETA AI.





This module provides comprehensive compliance monitoring including:


- SOC2, GDPR, HIPAA compliance tracking


- Automated compliance reporting


- Policy enforcement monitoring


- Audit trail generation


- Compliance dashboard and metrics


"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from enum import Enum
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field
import ValueError
import a
import affected_systems
import assessor
import bool
import category
import category_findings_list
import control_id
import description
import dict
import due_date
import evidence
import f
import finding_id
import finding_text
import findings
import float
import format_type
import framework
import generated_by
import int
import kwargs
import len
import list
import owner
import period_end
import period_start
import remediation_plan
import report_type
import requirements
import resolution_notes
import resolved_by
import risk_description
import round
import score
import self
import severity
import status
import str
import sum
import title


class ComplianceFramework(str, Enum):
    """Supported compliance frameworks."""

    SOC2 = "soc2"

    GDPR = "gdpr"

    HIPAA = "hipaa"

    PCI_DSS = "pci_dss"

    ISO27001 = "iso27001"

    NIST = "nist"

    CCPA = "ccpa"


class ComplianceStatus(str, Enum):
    """Compliance status values."""

    COMPLIANT = "compliant"

    NON_COMPLIANT = "non_compliant"

    PARTIAL = "partial"

    UNKNOWN = "unknown"

    REMEDIATION_REQUIRED = "remediation_required"


class ControlCategory(str, Enum):
    """Control categories."""

    ACCESS_CONTROL = "access_control"

    DATA_PROTECTION = "data_protection"

    AUDIT_LOGGING = "audit_logging"

    NETWORK_SECURITY = "network_security"

    ENCRYPTION = "encryption"

    INCIDENT_RESPONSE = "incident_response"

    BUSINESS_CONTINUITY = "business_continuity"

    CHANGE_MANAGEMENT = "change_management"

    VENDOR_MANAGEMENT = "vendor_management"

    RISK_MANAGEMENT = "risk_management"


class Severity(str, Enum):
    """Finding severity levels."""

    LOW = "low"

    MEDIUM = "medium"

    HIGH = "high"

    CRITICAL = "critical"


class ComplianceControl(BaseModel):
    """Compliance control definition."""

    control_id: str

    framework: ComplianceFramework

    category: ControlCategory

    title: str

    description: str

    requirements: list[str]

    implementation_guidance: str | None = None

    testing_procedures: list[str] = Field(default_factory=list)

    frequency: str = Field(
        default="quarterly"
    )  # daily, weekly, monthly, quarterly, annually

    owner: str | None = None

    automated: bool = Field(default=False)

    enabled: bool = Field(default=True)


class ComplianceAssessment(BaseModel):
    """Compliance assessment result."""

    assessment_id: str = Field(default_factory=lambda: str(uuid4()))

    control_id: str

    framework: ComplianceFramework

    status: ComplianceStatus

    score: float = Field(ge=0.0, le=100.0)

    findings: list[str] = Field(default_factory=list)

    evidence: list[str] = Field(default_factory=list)

    remediation_actions: list[str] = Field(default_factory=list)

    assessor: str | None = None

    assessment_date: datetime = Field(default_factory=lambda: datetime.now(UTC))

    next_assessment_due: datetime | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


class ComplianceFinding(BaseModel):
    """Compliance finding or issue."""

    finding_id: str = Field(default_factory=lambda: str(uuid4()))

    control_id: str

    framework: ComplianceFramework

    category: ControlCategory

    severity: Severity

    title: str

    description: str

    risk_description: str

    affected_systems: list[str] = Field(default_factory=list)

    evidence: list[str] = Field(default_factory=list)

    remediation_plan: str | None = None

    due_date: datetime | None = None

    owner: str | None = None

    status: str = Field(default="open")  # open, in_progress, resolved, closed

    discovered_date: datetime = Field(default_factory=lambda: datetime.now(UTC))

    resolved_date: datetime | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)


class ComplianceReport(BaseModel):
    """Compliance report."""

    report_id: str = Field(default_factory=lambda: str(uuid4()))

    framework: ComplianceFramework

    report_type: str = Field(
        default="assessment"
    )  # assessment, gap_analysis, remediation

    title: str

    description: str | None = None

    period_start: datetime

    period_end: datetime

    generated_date: datetime = Field(default_factory=lambda: datetime.now(UTC))

    generated_by: str | None = None

    # Summary metrics

    total_controls: int = Field(default=0)

    compliant_controls: int = Field(default=0)

    non_compliant_controls: int = Field(default=0)

    overall_score: float = Field(default=0.0, ge=0.0, le=100.0)

    # Detailed data

    assessments: list[ComplianceAssessment] = Field(default_factory=list)

    findings: list[ComplianceFinding] = Field(default_factory=list)

    recommendations: list[str] = Field(default_factory=list)

    # Metadata

    metadata: dict[str, Any] = Field(default_factory=dict)


class ComplianceManager:
    """Comprehensive compliance management system."""

    def __init__(self):
        """Initialize compliance manager."""

        self._controls: dict[str, ComplianceControl] = {}

        self._assessments: list[ComplianceAssessment] = []

        self._findings: list[ComplianceFinding] = []

        self._reports: list[ComplianceReport] = []

        # Load default control frameworks

        self._load_default_controls()

    def _load_default_controls(self) -> None:
        """Load default compliance controls for supported frameworks."""

        # SOC2 Type II Controls

        soc2_controls = [
            ComplianceControl(
                control_id="CC6.1",
                framework=ComplianceFramework.SOC2,
                category=ControlCategory.ACCESS_CONTROL,
                title="Logical Access Controls",
                description="The entity implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events to meet the entity's objectives.",
                requirements=[
                    "Implement user access management processes",
                    "Configure access controls for systems and data",
                    "Regularly review and update access permissions",
                    "Implement strong authentication mechanisms",
                ],
                testing_procedures=[
                    "Review user access management procedures",
                    "Test access control configurations",
                    "Verify authentication mechanisms",
                ],
            ),
            ComplianceControl(
                control_id="CC6.7",
                framework=ComplianceFramework.SOC2,
                category=ControlCategory.DATA_PROTECTION,
                title="Data Transmission and Disposal",
                description="The entity restricts the transmission, movement, and removal of information to authorized internal and external users and processes, and protects it during transmission, movement, or removal to meet the entity's objectives.",
                requirements=[
                    "Encrypt data in transit",
                    "Secure data transmission channels",
                    "Implement secure data disposal procedures",
                    "Control data movement and removal",
                ],
                testing_procedures=[
                    "Verify encryption of data in transit",
                    "Test secure transmission channels",
                    "Review data disposal procedures",
                ],
            ),
            ComplianceControl(
                control_id="A1.2",
                framework=ComplianceFramework.SOC2,
                category=ControlCategory.AUDIT_LOGGING,
                title="System Monitoring",
                description="The entity implements detection and monitoring procedures to identify (1) changes to configurations that result in the introduction of new vulnerabilities, and (2) susceptibilities to newly discovered vulnerabilities.",
                requirements=[
                    "Implement comprehensive logging",
                    "Monitor system activities and events",
                    "Detect configuration changes",
                    "Alert on security vulnerabilities",
                ],
                testing_procedures=[
                    "Review logging configurations",
                    "Test monitoring and alerting systems",
                    "Verify event detection capabilities",
                ],
            ),
        ]

        # GDPR Controls

        gdpr_controls = [
            ComplianceControl(
                control_id="GDPR.32",
                framework=ComplianceFramework.GDPR,
                category=ControlCategory.DATA_PROTECTION,
                title="Security of Processing",
                description="The controller and the processor shall implement appropriate technical and organizational measures to ensure a level of security appropriate to the risk.",
                requirements=[
                    "Implement data encryption",
                    "Ensure confidentiality and integrity",
                    "Implement access controls",
                    "Regular security testing and evaluation",
                ],
                testing_procedures=[
                    "Verify encryption implementation",
                    "Test access control mechanisms",
                    "Review security testing procedures",
                ],
            ),
            ComplianceControl(
                control_id="GDPR.25",
                framework=ComplianceFramework.GDPR,
                category=ControlCategory.DATA_PROTECTION,
                title="Data Protection by Design and by Default",
                description="The controller shall implement appropriate technical and organisational measures to show that processing is performed in accordance with this Regulation.",
                requirements=[
                    "Implement privacy by design",
                    "Default privacy settings",
                    "Data minimization principles",
                    "Purpose limitation",
                ],
                testing_procedures=[
                    "Review privacy design documentation",
                    "Test default privacy settings",
                    "Verify data minimization practices",
                ],
            ),
        ]

        # HIPAA Controls

        hipaa_controls = [
            ComplianceControl(
                control_id="164.312.a.1",
                framework=ComplianceFramework.HIPAA,
                category=ControlCategory.ACCESS_CONTROL,
                title="Access Control",
                description="Implement technical policies and procedures for electronic information systems that maintain electronic protected health information to allow access only to those persons or software programs that have been granted access rights.",
                requirements=[
                    "Implement unique user identification",
                    "Implement emergency access procedures",
                    "Implement automatic logoff",
                    "Implement encryption and decryption",
                ],
                testing_procedures=[
                    "Verify user identification mechanisms",
                    "Test emergency access procedures",
                    "Verify automatic logoff functionality",
                    "Test encryption implementation",
                ],
            ),
            ComplianceControl(
                control_id="164.312.b",
                framework=ComplianceFramework.HIPAA,
                category=ControlCategory.AUDIT_LOGGING,
                title="Audit Controls",
                description="Implement hardware, software, and/or procedural mechanisms that record and examine activity in information systems that contain or use electronic protected health information.",
                requirements=[
                    "Implement audit logging mechanisms",
                    "Record access to PHI",
                    "Review audit logs regularly",
                    "Protect audit log integrity",
                ],
                testing_procedures=[
                    "Verify audit logging implementation",
                    "Test audit log generation",
                    "Review audit log review procedures",
                ],
            ),
        ]

        # Add all controls

        all_controls = soc2_controls + gdpr_controls + hipaa_controls

        for control in all_controls:
            self._controls[control.control_id] = control

    def add_control(self, control: ComplianceControl) -> None:
        """Add a compliance control.





        Args:


            control: Compliance control to add


        """

        self._controls[control.control_id] = control

    def get_control(self, control_id: str) -> ComplianceControl | None:
        """Get a compliance control by ID.





        Args:


            control_id: Control ID





        Returns:


            Compliance control if found


        """

        return self._controls.get(control_id)

    def get_controls_by_framework(
        self, framework: ComplianceFramework
    ) -> list[ComplianceControl]:
        """Get all controls for a framework.





        Args:


            framework: Compliance framework





        Returns:


            List of compliance controls


        """

        return [
            control
            for control in self._controls.values()
            if control.framework == framework and control.enabled
        ]

    def conduct_assessment(
        self,
        control_id: str,
        status: ComplianceStatus,
        score: float,
        findings: list[str] | None = None,
        evidence: list[str] | None = None,
        assessor: str | None = None,
    ) -> ComplianceAssessment:
        """Conduct a compliance assessment for a control.





        Args:


            control_id: Control ID to assess


            status: Assessment status


            score: Compliance score (0-100)


            findings: Assessment findings


            evidence: Supporting evidence


            assessor: Person conducting assessment





        Returns:


            Compliance assessment


        """

        control = self.get_control(control_id)

        if not control:
            raise ValueError(f"Control {control_id} not found")

        # Calculate next assessment due date based on frequency

        frequency_days = {
            "daily": 1,
            "weekly": 7,
            "monthly": 30,
            "quarterly": 90,
            "annually": 365,
        }

        days_to_add = frequency_days.get(control.frequency, 90)

        next_due = datetime.now(UTC) + timedelta(days=days_to_add)

        assessment = ComplianceAssessment(
            control_id=control_id,
            framework=control.framework,
            status=status,
            score=score,
            findings=findings or [],
            evidence=evidence or [],
            assessor=assessor,
            next_assessment_due=next_due,
        )

        self._assessments.append(assessment)

        # Create findings for non-compliant assessments

        if status in [
            ComplianceStatus.NON_COMPLIANT,
            ComplianceStatus.REMEDIATION_REQUIRED,
        ]:
            for finding_text in findings or []:
                self.create_finding(
                    control_id=control_id,
                    title=f"Non-compliance: {control.title}",
                    description=finding_text,
                    severity=Severity.HIGH
                    if status == ComplianceStatus.NON_COMPLIANT
                    else Severity.MEDIUM,
                )

        return assessment

    def create_finding(
        self,
        control_id: str,
        title: str,
        description: str,
        severity: Severity,
        risk_description: str | None = None,
        affected_systems: list[str] | None = None,
        remediation_plan: str | None = None,
        due_date: datetime | None = None,
        owner: str | None = None,
    ) -> ComplianceFinding:
        """Create a compliance finding.





        Args:


            control_id: Associated control ID


            title: Finding title


            description: Finding description


            severity: Finding severity


            risk_description: Risk description


            affected_systems: Affected systems


            remediation_plan: Remediation plan


            due_date: Remediation due date


            owner: Finding owner





        Returns:


            Compliance finding


        """

        control = self.get_control(control_id)

        if not control:
            raise ValueError(f"Control {control_id} not found")

        finding = ComplianceFinding(
            control_id=control_id,
            framework=control.framework,
            category=control.category,
            severity=severity,
            title=title,
            description=description,
            risk_description=risk_description or description,
            affected_systems=affected_systems or [],
            remediation_plan=remediation_plan,
            due_date=due_date,
            owner=owner,
        )

        self._findings.append(finding)

        return finding

    def resolve_finding(
        self,
        finding_id: str,
        resolution_notes: str | None = None,
        resolved_by: str | None = None,
    ) -> bool:
        """Resolve a compliance finding.





        Args:


            finding_id: Finding ID to resolve


            resolution_notes: Resolution notes


            resolved_by: Person resolving the finding





        Returns:


            True if finding was resolved


        """

        for finding in self._findings:
            if finding.finding_id == finding_id:
                finding.status = "resolved"

                finding.resolved_date = datetime.now(UTC)

                if resolution_notes:
                    finding.metadata["resolution_notes"] = resolution_notes

                if resolved_by:
                    finding.metadata["resolved_by"] = resolved_by

                return True

        return False

    def generate_compliance_report(
        self,
        framework: ComplianceFramework,
        period_start: datetime,
        period_end: datetime,
        report_type: str = "assessment",
        title: str | None = None,
        generated_by: str | None = None,
    ) -> ComplianceReport:
        """Generate a compliance report.





        Args:


            framework: Compliance framework


            period_start: Report period start


            period_end: Report period end


            report_type: Type of report


            title: Report title


            generated_by: Report generator





        Returns:


            Compliance report


        """

        # Get assessments for the framework and period

        relevant_assessments = [
            assessment
            for assessment in self._assessments
            if (
                assessment.framework == framework
                and period_start <= assessment.assessment_date <= period_end
            )
        ]

        # Get findings for the framework and period

        relevant_findings = [
            finding
            for finding in self._findings
            if (
                finding.framework == framework
                and period_start <= finding.discovered_date <= period_end
            )
        ]

        # Calculate summary metrics

        total_controls = len(self.get_controls_by_framework(framework))

        compliant_controls = len(
            [a for a in relevant_assessments if a.status == ComplianceStatus.COMPLIANT]
        )

        non_compliant_controls = len(
            [
                a
                for a in relevant_assessments
                if a.status == ComplianceStatus.NON_COMPLIANT
            ]
        )

        # Calculate overall score

        if relevant_assessments:
            overall_score = sum(a.score for a in relevant_assessments) / len(
                relevant_assessments
            )

        else:
            overall_score = 0.0

        # Generate recommendations

        recommendations = self._generate_recommendations(framework, relevant_findings)

        report = ComplianceReport(
            framework=framework,
            report_type=report_type,
            title=title or f"{framework.value.upper()} Compliance Report",
            period_start=period_start,
            period_end=period_end,
            generated_by=generated_by,
            total_controls=total_controls,
            compliant_controls=compliant_controls,
            non_compliant_controls=non_compliant_controls,
            overall_score=overall_score,
            assessments=relevant_assessments,
            findings=relevant_findings,
            recommendations=recommendations,
        )

        self._reports.append(report)

        return report

    def _generate_recommendations(
        self, framework: ComplianceFramework, findings: list[ComplianceFinding]
    ) -> list[str]:
        """Generate recommendations based on findings.





        Args:


            framework: Compliance framework


            findings: List of findings





        Returns:


            List of recommendations


        """

        recommendations = []

        # Group findings by category

        category_findings = {}

        for finding in findings:
            if finding.category not in category_findings:
                category_findings[finding.category] = []

            category_findings[finding.category].append(finding)

        # Generate category-specific recommendations

        for category, category_findings_list in category_findings.items():
            high_severity_count = len(
                [
                    f
                    for f in category_findings_list
                    if f.severity in [Severity.HIGH, Severity.CRITICAL]
                ]
            )

            if high_severity_count > 0:
                if category == ControlCategory.ACCESS_CONTROL:
                    recommendations.append(
                        f"Prioritize remediation of {high_severity_count} high-severity "
                        "access control findings. Review user access management processes "
                        "and implement stronger authentication mechanisms."
                    )

                elif category == ControlCategory.DATA_PROTECTION:
                    recommendations.append(
                        f"Address {high_severity_count} critical data protection issues. "
                        "Implement additional encryption controls and review data handling procedures."
                    )

                elif category == ControlCategory.AUDIT_LOGGING:
                    recommendations.append(
                        f"Resolve {high_severity_count} audit logging deficiencies. "
                        "Enhance monitoring capabilities and implement comprehensive logging."
                    )

        # Framework-specific recommendations

        if framework == ComplianceFramework.SOC2:
            recommendations.append(
                "Conduct regular SOC2 readiness assessments and maintain continuous monitoring "
                "of security controls to ensure ongoing compliance."
            )

        elif framework == ComplianceFramework.GDPR:
            recommendations.append(
                "Implement privacy impact assessments for new data processing activities "
                "and maintain documentation of data processing activities."
            )

        elif framework == ComplianceFramework.HIPAA:
            recommendations.append(
                "Conduct regular risk assessments for PHI handling and implement "
                "additional safeguards for electronic protected health information."
            )

        return recommendations

    def get_compliance_dashboard(self) -> dict[str, Any]:
        """Get compliance dashboard data.





        Returns:


            Dictionary with dashboard data


        """

        dashboard_data = {}

        # Overall compliance status by framework

        for framework in ComplianceFramework:
            recent_assessments = [
                a
                for a in self._assessments
                if (
                    a.framework == framework
                    and a.assessment_date > datetime.now(UTC) - timedelta(days=90)
                )
            ]

            if recent_assessments:
                avg_score = sum(a.score for a in recent_assessments) / len(
                    recent_assessments
                )

                compliant_count = len(
                    [
                        a
                        for a in recent_assessments
                        if a.status == ComplianceStatus.COMPLIANT
                    ]
                )

                total_count = len(recent_assessments)

                dashboard_data[framework.value] = {
                    "average_score": round(avg_score, 1),
                    "compliance_rate": round((compliant_count / total_count) * 100, 1),
                    "total_assessments": total_count,
                    "compliant_assessments": compliant_count,
                }

        # Open findings by severity

        open_findings = [
            f for f in self._findings if f.status in ["open", "in_progress"]
        ]

        findings_by_severity = {
            severity.value: len([f for f in open_findings if f.severity == severity])
            for severity in Severity
        }

        dashboard_data["findings"] = {
            "total_open": len(open_findings),
            "by_severity": findings_by_severity,
        }

        # Recent activity

        recent_date = datetime.now(UTC) - timedelta(days=30)

        recent_assessments = [
            a for a in self._assessments if a.assessment_date > recent_date
        ]

        recent_findings = [f for f in self._findings if f.discovered_date > recent_date]

        dashboard_data["recent_activity"] = {
            "assessments_last_30_days": len(recent_assessments),
            "findings_last_30_days": len(recent_findings),
        }

        return dashboard_data

    def export_compliance_data(self, format_type: str = "json") -> str:
        """Export compliance data.





        Args:


            format_type: Export format (json, csv)





        Returns:


            Exported data as string


        """

        export_data = {
            "controls": [control.dict() for control in self._controls.values()],
            "assessments": [assessment.dict() for assessment in self._assessments],
            "findings": [finding.dict() for finding in self._findings],
            "reports": [report.dict() for report in self._reports],
        }

        if format_type == "json":
            return json.dumps(export_data, default=str, indent=2)

        else:
            raise ValueError(f"Unsupported export format: {format_type}")


# Factory functions


def create_compliance_manager() -> ComplianceManager:
    """Create compliance manager instance.





    Returns:


        ComplianceManager instance


    """

    return ComplianceManager()


def create_compliance_control(
    control_id: str,
    framework: ComplianceFramework,
    category: ControlCategory,
    title: str,
    description: str,
    requirements: list[str],
    **kwargs,
) -> ComplianceControl:
    """Create compliance control.





    Args:


        control_id: Control ID


        framework: Compliance framework


        category: Control category


        title: Control title


        description: Control description


        requirements: Control requirements


        **kwargs: Additional control parameters





    Returns:


        Compliance control


    """

    return ComplianceControl(
        control_id=control_id,
        framework=framework,
        category=category,
        title=title,
        description=description,
        requirements=requirements,
        **kwargs,
    )
