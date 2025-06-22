document.addEventListener('DOMContentLoaded', () => {
    // Initialize Materialize components
    const elems = document.querySelectorAll('.modal');
    M.Modal.init(elems);

    const urlParams = new URLSearchParams(window.location.search);
    const recipientId = urlParams.get('id'); // e.g., f47ac10b

    if (recipientId) {
        const repoName = 'certificates';
        const assertionUrl = `/${repoName}/public_html/assertions/Test Badge Name/${recipientId}.json`;
        const certificatePdfUrl = `/${repoName}/public_html/certificates/Test/${recipientId}_certificate.pdf`;
        const certificateImageUrl = `/${repoName}/public_html/certificates/Test/${recipientId}_certificate.png`;

        fetch(assertionUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('recipient-name').innerHTML = `Certificate Issued to <strong>${data.recipient.identity}</strong>`;
                document.getElementById('badge-name').textContent = data.badge.name;
                document.getElementById('issuer-name').textContent = data.badge.issuer.name;
                
                // Use innerHTML to parse the HTML tags in the description
                document.getElementById('badge-description').innerHTML = data.badge.description;
                document.getElementById('earning-criteria').innerHTML = data.badge.criteria.narrative;
                
                const issuedOnDate = new Date(data.issuedOn).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
                
                document.getElementById('certificate-image').src = certificateImageUrl;

                const skillsList = document.getElementById('skills-list');
                skillsList.innerHTML = ''; // Clear existing skills
                if (data.badge.tags && Array.isArray(data.badge.tags)) {
                    data.badge.tags.forEach(tag => {
                        const chip = document.createElement('div');
                        chip.className = 'chip';
                        chip.textContent = tag;
                        skillsList.appendChild(chip);
                    });
                }

                // Populate Modal
                document.getElementById('modal-recipient-name').textContent = data.recipient.identity;
                document.getElementById('modal-signatory').textContent = "Rajiv Sharma"; // Placeholder
                document.getElementById('modal-issue-date').textContent = issuedOnDate;
                document.getElementById('modal-assertion-id').textContent = data.id;

                // Re-initialize modal with content
                const modal_elems = document.querySelectorAll('.modal');
                M.Modal.init(modal_elems);

                // --- New Actions Logic ---
                const pageUrl = window.location.href;

                // 1. Download Action
                document.getElementById('action-download').href = certificatePdfUrl;

                // 2. Add to LinkedIn Profile Action
                const linkedInUrl = new URL('https://www.linkedin.com/profile/add');
                linkedInUrl.searchParams.append('startTask', data.badge.name);
                linkedInUrl.searchParams.append('name', data.badge.name);
                // Note: Finding organizationId usually requires an API lookup. We'll use the name.
                // linkedInUrl.searchParams.append('organizationName', data.badge.issuer.name);
                const issueDate = new Date(data.issuedOn);
                linkedInUrl.searchParams.append('issueYear', issueDate.getFullYear());
                linkedInUrl.searchParams.append('issueMonth', issueDate.getMonth() + 1);
                linkedInUrl.searchParams.append('certUrl', pageUrl);
                linkedInUrl.searchParams.append('certId', data.id);
                document.getElementById('action-add-to-profile').href = linkedInUrl.href;

                // 3. Share Action (Copy to Clipboard)
                document.getElementById('action-share').addEventListener('click', (e) => {
                    e.preventDefault();
                    navigator.clipboard.writeText(pageUrl).then(() => {
                        M.toast({html: 'Link copied to clipboard!'})
                    }).catch(err => {
                        console.error('Could not copy text: ', err);
                        M.toast({html: 'Failed to copy link.'})
                    });
                });

            })
            .catch(error => {
                console.error('Error fetching assertion data:', error);
                document.querySelector('.container').innerHTML = '<h1>Error loading certificate data.</h1>';
            });
    } else {
        document.querySelector('.container').innerHTML = '<h1>No recipient specified.</h1>';
    }
}); 