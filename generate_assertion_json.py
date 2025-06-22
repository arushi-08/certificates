import json
from datetime import datetime

from generate_certificate import create_directory_if_not_exists


def create_assertion(recipient_name, recipient_identity, badge_name, badge_id, issuer_id, image_url, assertion_id):
    assertion = {
        "@context": "https://w3id.org/openbadges/v2",
        "type": "Assertion",
        "id": assertion_id,
        "issuedOn": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),
        "recipient": {
            "identity": recipient_identity,
            "type": "ID"
        },
        "badge": {
            "id": badge_id,
            "name": badge_name,
            "description": "<p><strong>Elevate Your Potential with NLP</strong></p>\r\n\r\n<p>This high-impact NLP workshop is designed to help professionals improve communication, leadership, and influence using proven Neuro-Linguistic Programming (NLP) techniques.</p>\r\n\r\n<p><strong>Key Learnings:</strong></p>\r\n\r\n<ul>\r\n\t<li>Envisioning Success: Use visualization to achieve clarity, motivation, and focus.</li>\r\n\t<li>Quick Thinking &amp; Mental Agility: Enhance adaptability, problem-solving, and creativity.</li>\r\n\t<li>NLP Influence Techniques: Master anchoring, mirroring, reframing, and rapport-building.</li>\r\n\t<li>Effective Communication: Learn Visual, Auditory, and Kinesthetic (VAK) communication styles.</li>\r\n\t<li>Leadership &amp; Team Synergy: Strengthen collaboration, persuasion, and decision-making.</li>\r\n\t<li>Emotional Control &amp; Resilience: Manage stress, stay composed, and handle workplace challenges.</li>\r\n\t<li>Hypnotic Induction for Focus: Experience NLP-based deep focus and learning techniques.</li>\r\n</ul>\r\n\r\n<p>Total Duration: 1 Day</p>\r\n\r\n<p>&nbsp;</p>\r\n", 
            "image": image_url,
            "issuer": {
                "id": issuer_id,
                "name": "NLP Limited.com",
                "type": "Profile",
                "url": "https://www.nlplimited.com"
            },
            "criteria": {
                "narrative": "<p>To earn the certificate, the participant has to complete the following:</p>\r\n\r\n<ol>\r\n\t<li>Filling the Pre-workshop Form</li>\r\n\t<li>Active Participation during the Workshop</li>\r\n\t<li>Follow up with the Coach and Trainer</li>\r\n</ol>\r\n"
            },
            "type": "BadgeClass"
        },
        "verification": {
            "type": "hosted"
        }
    }
    return assertion

def main():
    # badge_name = "Elevate Your Potential With NLP"
    badge_name = 'Test Badge Name'
    recipient_identity="1001"
    recipient_name = "Alice Smith"
    # Example usage
    assertion = create_assertion(
        recipient_name=recipient_name,
        recipient_identity=recipient_identity,
        badge_name=badge_name,
        badge_id="https://nlplimited.com/badgeClasses/123",
        issuer_id="https://nlplimited.com/profiles/issuer",
        image_url=f"https://nlplimited.com/certificates/{recipient_identity}_badge.png",
        assertion_id="https://nlplimited.com/assertions/uuid"
    )

    create_directory_if_not_exists(f'public_html/assertions/{badge_name}')
    with open(f'public_html/assertions/{badge_name}/{recipient_name}.json', 'w') as f:
        json.dump(assertion, f, indent=2)


if __name__ == '__main__':
    main()