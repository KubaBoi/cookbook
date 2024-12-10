/**
 * Nacita a stavi seznam receptu
 */

async function getRecipes()
{
    var response = await callEndpoint("GET", "/recipes/get");
    if (response.ERROR == null) {
        return response;
    }
    else {
        alert(response.ERROR);
    }
}

async function buildRecipes()
{
    recps = await getRecipes();
    if (recps == null)
        return;

    let table = document.getElementById("recipes_table");
    clearTable(table);
    recps.recipes_names.forEach(element => {
        addRow(table, [{text: element, 
                attributes: [
                    {
                        name: "onclick", 
                        value: "buildRecipe('" + element + "')"
                    }
                ]
            }
        ]);
    });
}