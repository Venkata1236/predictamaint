const MaintenanceTicket = ({
    incident,
}) => {

    if (!incident) {
        return null
    }

    return (

        <div
            style={{
                background: "#1e293b",
                padding: "20px",
                borderRadius: "16px",
                marginTop: "20px",
                border: "2px solid #ef4444",
            }}
        >

            <h2
                style={{
                    marginBottom: "20px",
                    color: "#ef4444",
                }}
            >
                Maintenance Ticket
            </h2>

            <p>
                <strong>
                    Machine:
                </strong>
                {" "}
                {incident.machine_id}
            </p>

            <p
                style={{
                    marginTop: "10px",
                }}
            >
                <strong>
                    Alert Tier:
                </strong>
                {" "}
                {incident.alert_tier}
            </p>

            <p
                style={{
                    marginTop: "10px",
                }}
            >
                <strong>
                    Risk Score:
                </strong>
                {" "}
                {
                    (
                        incident
                        .ensemble_score
                        * 100
                    ).toFixed(2)
                }%
            </p>

            <p
                style={{
                    marginTop: "10px",
                }}
            >
                <strong>
                    Affected Sensors:
                </strong>
                {" "}
                {
                    incident
                    .anomalous_features
                    .join(", ")
                }
            </p>

            <p
                style={{
                    marginTop: "10px",
                }}
            >
                <strong>
                    Recommended Action:
                </strong>
                {" "}
                Inspect machine and
                schedule preventive
                maintenance.
            </p>

        </div>
    )
}

export default MaintenanceTicket