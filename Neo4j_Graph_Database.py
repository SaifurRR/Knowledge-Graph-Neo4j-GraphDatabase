{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": []
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "code",
      "source": [
        "pip install neo4j\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "XO5KP-gHSq7Q",
        "outputId": "e15192e4-f7d7-4a7e-8177-e2a58e44f192"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Collecting neo4j\n",
            "  Downloading neo4j-5.15.0.tar.gz (196 kB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m196.5/196.5 kB\u001b[0m \u001b[31m2.4 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25h  Installing build dependencies ... \u001b[?25l\u001b[?25hdone\n",
            "  Getting requirements to build wheel ... \u001b[?25l\u001b[?25hdone\n",
            "  Installing backend dependencies ... \u001b[?25l\u001b[?25hdone\n",
            "  Preparing metadata (pyproject.toml) ... \u001b[?25l\u001b[?25hdone\n",
            "Requirement already satisfied: pytz in /usr/local/lib/python3.10/dist-packages (from neo4j) (2023.3.post1)\n",
            "Building wheels for collected packages: neo4j\n",
            "  Building wheel for neo4j (pyproject.toml) ... \u001b[?25l\u001b[?25hdone\n",
            "  Created wheel for neo4j: filename=neo4j-5.15.0-py3-none-any.whl size=272484 sha256=183d7ecf1bcac71216856e96c6d564e4f455f21df21de617acea5b7bdecd5945\n",
            "  Stored in directory: /root/.cache/pip/wheels/d5/08/10/6371dbdeec2efd7782f559b21c32bb6b4192ae0216ec5e39c5\n",
            "Successfully built neo4j\n",
            "Installing collected packages: neo4j\n",
            "Successfully installed neo4j-5.15.0\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "pip install --upgrade neo4j\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "kvoAi1UsVmK_",
        "outputId": "8b2a12fa-6f73-4576-eeb0-dbdb46fa5706"
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Requirement already satisfied: neo4j in /usr/local/lib/python3.10/dist-packages (5.15.0)\n",
            "Requirement already satisfied: pytz in /usr/local/lib/python3.10/dist-packages (from neo4j) (2023.3.post1)\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "from neo4j import GraphDatabase\n",
        "\n",
        "class CybersecurityGraph:\n",
        "    def __init__(self, uri, user, password):\n",
        "        self._driver = GraphDatabase.driver(uri, auth=(user, password))\n",
        "\n",
        "    def close(self):\n",
        "        self._driver.close()\n",
        "\n",
        "    def create_graph(self):\n",
        "        with self._driver.session() as session:\n",
        "            # Create entities\n",
        "            session.run(\"\"\"\n",
        "                CREATE (threatActor:ThreatActor {name: 'APT1', description: 'Advanced Persistent Threat Group 1', motivation: 'Espionage', sophistication: 'High'})\n",
        "                CREATE (attackTechnique:AttackTechnique {name: 'Phishing', description: 'Social Engineering Attack', mitigation: 'User Training'})\n",
        "                CREATE (vulnerability:Vulnerability {name: 'CVE-2023-1234', description: 'Security Vulnerability', severity: 'High'})\n",
        "                CREATE (asset:Asset {name: 'Server-001', description: 'Web Server', criticality: 'High'})\n",
        "                CREATE (incident:Incident {date: '2023-12-15', description: 'Data Breach'})\n",
        "            \"\"\")\n",
        "\n",
        "            # Create relationships\n",
        "            session.run(\"\"\"\n",
        "                MATCH (threatActor:ThreatActor), (attackTechnique:AttackTechnique)\n",
        "                WHERE threatActor.name = 'APT1' AND attackTechnique.name = 'Phishing'\n",
        "                CREATE (threatActor)-[:USES_ATTACK_TECHNIQUE]->(attackTechnique)\n",
        "            \"\"\")\n",
        "\n",
        "            session.run(\"\"\"\n",
        "                MATCH (attackTechnique:AttackTechnique), (vulnerability:Vulnerability)\n",
        "                WHERE attackTechnique.name = 'Phishing' AND vulnerability.name = 'CVE-2023-1234'\n",
        "                CREATE (attackTechnique)-[:EXPLOITS_VULNERABILITY]->(vulnerability)\n",
        "            \"\"\")\n",
        "\n",
        "            session.run(\"\"\"\n",
        "                MATCH (vulnerability:Vulnerability), (asset:Asset)\n",
        "                WHERE vulnerability.name = 'CVE-2023-1234' AND asset.name = 'Server-001'\n",
        "                CREATE (vulnerability)-[:AFFECTS_ASSET]->(asset)\n",
        "            \"\"\")\n",
        "\n",
        "            session.run(\"\"\"\n",
        "                MATCH (attackTechnique:AttackTechnique), (incident:Incident), (asset:Asset)\n",
        "                WHERE attackTechnique.name = 'Phishing' AND incident.date = '2023-12-15' AND asset.name = 'Server-001'\n",
        "                CREATE (attackTechnique)-[:RESULTS_IN_INCIDENT]->(incident), (incident)-[:AFFECTS_ASSET]->(asset)\n",
        "            \"\"\")\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    uri = \"bolt://localhost:7687\"  # Change this to your Neo4j URI\n",
        "    user = \"neo4j\"  # Change this to your Neo4j username\n",
        "    password = \"password\"  # Change this to your Neo4j password\n",
        "\n",
        "    graph = CybersecurityGraph(uri, user, password)\n",
        "    graph.create_graph()\n",
        "    graph.close()\n"
      ],
      "metadata": {
        "id": "uRSa7F5yT57s"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "from neo4j import GraphDatabase\n",
        "\n",
        "\n",
        "\n",
        "if __name__ == \"__main__\":\n",
        "    uri = \"bolt://localhost:7687\"\n",
        "    user = \"neo4j\"\n",
        "    password = \"password\"\n",
        "\n",
        "    try:\n",
        "        graph = CybersecurityGraph(uri, user, password)\n",
        "        graph.create_graph()\n",
        "        graph.close()\n",
        "        print(\"Connection successful!\")\n",
        "    except Exception as e:\n",
        "        print(f\"Error: {e}\")\n"
      ],
      "metadata": {
        "id": "Agf9rjmLT59z",
        "outputId": "e71dce5d-7d0d-408a-c082-51a425c17b33",
        "colab": {
          "base_uri": "https://localhost:8080/"
        }
      },
      "execution_count": null,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Error: Couldn't connect to localhost:7687 (resolved to ()):\n",
            "Failed to establish connection to ResolvedIPv4Address(('127.0.0.1', 7687)) (reason [Errno 111] Connection refused)\n",
            "Failed to establish connection to ResolvedIPv6Address(('::1', 7687, 0, 0)) (reason [Errno 99] Cannot assign requested address)\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "phU3rWHlT6AT"
      },
      "execution_count": null,
      "outputs": []
    }
  ]
}
