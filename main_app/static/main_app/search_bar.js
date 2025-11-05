const input = document.getElementById('food-search');
const resultsList = document.getElementById('autocomplete-results');

input.addEventListener('keyup', function() {
    const query = this.value.trim();

    if (query.length === 0) {
        resultsList.style.display = 'none';
        resultsList.innerHTML = '';
        return;
    }

    fetch(`/foods/?q=${encodeURIComponent(query)}`, {
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(data => {
        resultsList.innerHTML = '';

        if (data.length > 0) {
           data.forEach(foodObj => {
            const li = document.createElement('li');
            li.textContent = foodObj.name;
            li.dataset.foodId = foodObj.id;
            li.addEventListener('click', () => {
                window.location.href = `/food/${foodObj.id}/`;
            });
            resultsList.appendChild(li);
});
        } else {
            const li = document.createElement('li');
            li.textContent = 'No foods found';
            li.style.color = 'gray';
            li.style.padding = '5px';
            resultsList.appendChild(li);
        }

        resultsList.style.display = 'block';
    });
});

