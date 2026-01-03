# User Role Access Model

## Background

The analytics platform supports several user communities—ETL engineers who build and schedule pipelines, developers and data scientists who author notebooks and experiments, analysts who design reports, and business consumers who view dashboards. Each community requires a different level of access to workspaces and underlying data. Granting too much access exposes engineering artefacts and sensitive data; granting too little blocks legitimate work. This section describes how to map each persona to Microsoft Fabric workspace roles and supplementary data-plane permissions while adhering to least privilege.

The approach relies on Microsoft Entra security groups assigned to workspace roles. Rather than adding named individuals, administrators add users to groups such as `Fabric-Gold-Contributor`, and those groups are granted the appropriate role. This pattern keeps membership auditable, simplifies lifecycle changes, and aligns with Microsoft's recommended governance model.

## Assign workspace roles (control-plane access)

Fabric enforces access through four workspace roles. Users without any role cannot see the workspace, so the role assignment becomes the primary control plane.

| Role | Typical persona | Key capabilities |
|------|-----------------|------------------|
| Admin | Platform owners | Manage capacity settings, customer-managed keys, deployment pipelines; grant and revoke access |
| Member | Centre-of-excellence leads | Reshare content, coordinate Git branches, supervise cross-team collaboration |
| Contributor | ETL engineers, developers, data scientists | Create and modify lakehouses, warehouses, notebooks, pipelines; read data via OneLake and SQL endpoints |
| Viewer | Analysts validating models | Browse items without default data-plane access; RLS remains enforceable |

Reserve Admin for a small platform team. Assign Member only where resharing or Git integration authority is required. Use Contributor for personas who build artefacts and need to validate outputs. Viewer suits analysts who must browse a workspace during model validation, yet it should not be the default route for broad consumption.

## Grant engineers build access (development workspaces)

ETL engineers and developers iterate on pipelines, notebooks, and lakehouses throughout the development lifecycle. In development and feature workspaces, grant Contributor so that they can create and modify items freely. Where Git integration is required, ensure at least Member access on the workspace that synchronises with the repository.

In test and production stages, reduce engineers to Contributor or Viewer depending on operational policy. Automated deployment pipelines—rather than individual users—should hold the write permissions needed to promote artefacts.

## Enable analysts to author reports (semantic model sharing)

Analysts typically need read access to curated semantic models and SQL endpoints rather than full workspace visibility. When collaboration during model validation is necessary, Viewer provides controlled browsing. In most cases, however, share the semantic model directly with Build permission so that analysts can author reports without seeing upstream pipelines or notebooks.

Before distributing a semantic model, configure row-level security (RLS) or object-level security (OLS) to restrict data visibility. Direct Lake semantic models should use a fixed identity or RLS to prevent report viewers from inheriting broader OneLake permissions than intended.

## Support data-science exploration (sandbox workspaces)

Data scientists often span exploratory and production workloads. Grant Contributor in sandbox or feature workspaces where experimentation is encouraged, then reduce to Viewer or SQL-only access in governed production workspaces. For read-only investigative querying, share the lakehouse or warehouse endpoint with the appropriate SQL permissions rather than assigning a workspace role.

## Deliver reports to consumers (Power BI apps)

Business consumers should remain outside engineering workspaces entirely. Distribute curated dashboards and reports through Power BI apps linked to gold workspaces or via cross-workspace semantic models. RLS ensures each consumer sees only the data slices relevant to their department without requiring individual permission grants.

When a consumer requires access to a single semantic model without workspace membership, share the item with `Read` or `ReadData` permission. This approach isolates exposure to the specific artefact while preserving governance over the rest of the workspace.

## Extend access to data (OneLake and SQL permissions)

Workspace roles govern control-plane visibility, but data-plane access requires additional attention. Contributors and higher roles inherit read rights to OneLake and SQL endpoints, whereas Viewers do not. To satisfy read-only analysts, layer OneLake security roles or explicit SQL GRANT statements on gold lakehouses and warehouses.

The following steps outline a typical data-plane extension for Viewer-level analysts:

1. Create an OneLake security role scoped to the required tables or folders.
2. Add the analyst security group to that role.
3. Grant SQL endpoint permissions where analysts also query via T-SQL.
4. Validate that RLS or OLS on any shared semantic model restricts rows and columns appropriately.

## Standardise security group naming (governance)

Create one Entra security group per workspace role and environment stage—for example, `Fabric-Gold-Contributor` or `Fabric-Dev-Viewer`. This naming convention clarifies intent during access reviews and supports automation through Fabric REST APIs or scripted group provisioning. Routine audits become straightforward because administrators review group membership rather than individual assignments.

---

## Microsoft References

- [Permission model](https://learn.microsoft.com/en-us/fabric/security/permission-model)
- [Roles in workspaces in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces)
- [Give users access to workspaces](https://learn.microsoft.com/en-us/fabric/fundamentals/give-access-workspaces)
- [OneLake security overview](https://learn.microsoft.com/en-us/fabric/onelake/security/get-started-security)
- [Power BI implementation planning: Workspaces](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-implementation-planning-workspaces-workspace-level-planning)
- [Microsoft Fabric end-to-end security scenario](https://learn.microsoft.com/en-us/fabric/security/security-scenario)
