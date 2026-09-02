const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function main() {
  console.log("=== TEST 1 : Lecture des départements ===");
  const departements = await prisma.departement.findMany();
  console.log(departements);

  console.log("\n=== TEST 2 : Lecture d'une application avec son département (relation) ===");
  const application = await prisma.application.findFirst({
    include: { departement: true }
  });
  console.log(application);

  console.log("\n=== TEST 3 : Création d'un département test ===");
  const nouveauDepartement = await prisma.departement.create({
    data: { nom_departement: "Test_Prisma" }
  });
  console.log("Créé :", nouveauDepartement);

  console.log("\n=== TEST 4 : Suppression du département test ===");
  const suppression = await prisma.departement.delete({
    where: { id_departement: nouveauDepartement.id_departement }
  });
  console.log("Supprimé :", suppression);
}

main()
  .catch((e) => console.error("Erreur :", e))
  .finally(async () => {
    await prisma.$disconnect();
  });