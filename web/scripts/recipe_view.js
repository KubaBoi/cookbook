/**
 * Nacita a stavi pohled na detail receptu
 */

async function getRecipe(name)
{
    var response = await callEndpoint("GET", "/recipes/get_recipe?name=" + name);
    if (response.ERROR == null) {
        return response;
    }
    else {
        alert(response.ERROR);
    }
}

async function buildRecipe(name) {
    recipe = await getRecipe(name);
    if (recipe == null)
    {
        alert("Recept nenalezen");
        return;
    }

    document.getElementById("recipe_name").textContent = recipe.name;
    document.getElementById("recipe_source").href = recipe.source;

    let ingTable = document.getElementById("recipe_ings");
    clearTable(ingTable);
    recipe.ingredients.forEach(element => {
        addRow(ingTable, [
            {text: element[1]},
            {text: element[0]}
        ]);
    });

    let stepsTable = document.getElementById("recipe_steps");
    clearTable(stepsTable);
    let i = 0;
    recipe.steps.forEach(element => {
        addRow(stepsTable, [
            {text: i++},
            {text: element}
        ])
    });
}