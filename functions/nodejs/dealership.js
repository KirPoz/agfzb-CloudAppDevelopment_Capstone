/*
 * Get all dealerships
 */
const Cloudant = require('@cloudant/cloudant');
async function main(params) {
    const cloudant = Cloudant({
        url: params.COUCH_URL,
        plugins: {
            iamauth: {
                iamApiKey: params.IAM_API_KEY
            }
        }
    });
    const dbDealerships = cloudant.db.use("dealerships")
    //const dbDealerships = cloudant.db.use("test")
    try {
        if (params.STATE) {
            var state = params.STATE;
            //state = state.replace(/[&\/\\#,+()$~%.'":*?<>{}]/g, '')
            state = state.replace(/[^a-zA-Z0-9]/g, '');
            try{
                let dbData = await dbDealerships.find({selector: {st: {"$eq": state}}});
                if (dbData.docs.length == 0) {
                    throw new Error("The database is empty");
                } else {
                    return {dbData: dbData.docs}
                }
            } catch (error) {
                return {
                    "Error status code":  "404",
                    "Error message": error.message
                }
            }
        } else {
            try {
                // extract all the data, including the document bodies
                let dbData = await dbDealerships.list({include_docs: true})
                // checking if there is data in the database?
                if (dbData.rows.length == 0) {
                    //let error = new Error("The database is empty");
                    throw new Error("The database is empty");
                } else {
                    // response.rows is an array with a 'doc' attribute for each document
                    let bdList = await dbData.rows.map((row) => {
                        return row.doc
                    });
                    return {bdList: bdList}
                }
            } catch (error) {
                return {
                    "Error status code":  "404",
                    "Error message": error.message
                }
            }
        }
    } catch (error) {
        return {
            error: error.description
        };
    }
};