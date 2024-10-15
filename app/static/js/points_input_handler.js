
document.addEventListener('DOMContentLoaded', function() {
    const addButton = document.getElementById('add-row');
    const removeButton = document.getElementById('remove-row');
    const inputRows = document.getElementById('input-rows');
    const operationSelect = document.getElementById('operation');

    addButton.addEventListener('click', function() {
        const newRow = document.createElement('div');
        newRow.className = 'input-row';
        newRow.innerHTML = `
            <input type="number" name="x[]" placeholder="x">
            <input type="number" name="y[]" placeholder="y">
            <input type="number" name="z[]" placeholder="z">
        `;
        inputRows.appendChild(newRow);
    });

    removeButton.addEventListener('click', function() {
        const rows = inputRows.getElementsByClassName('input-row');
        if (rows.length > 0) {
            inputRows.removeChild(rows[rows.length - 1]);
        }
    });

    operationSelect.addEventListener('change', function(event) {
        // value of selected opperation
        const selectedOperation = event.target.value;
        switch(selectedOperation) {
            case 'move_mesh':
                console.log('Move Mesh selected');
                // Add your logic for move mesh selection
                break;
            case 'rotate_mesh':
                console.log('Rotate Mesh selected');
                // Add your logic for rotate mesh selection
                break;
            case 'bounding_box':
                console.log('Bounding Box selected');
                // Add your logic for bounding box selection
                break;
            case 'check_convexity':
                console.log('Check Convexity selected');
                // Add your logic for check convexity selection
                break;
        }
    });
});
