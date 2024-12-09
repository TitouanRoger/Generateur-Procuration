import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Fonction pour générer la procuration
def generer_procuration():
    # Récupération des données saisies
    mandant_nom = entry_nom_mandant.get()
    mandant_prenom = entry_prenom_mandant.get()
    mandant_date_naissance = entry_date_naissance_mandant.get()
    mandant_lieu_naissance = entry_lieu_naissance_mandant.get()
    mandant_adresse = entry_adresse_mandant.get()
    mandataire_nom = entry_nom_mandataire.get()
    mandataire_prenom = entry_prenom_mandataire.get()
    mandataire_date_naissance = entry_date_naissance_mandataire.get()
    mandataire_lieu_naissance = entry_lieu_naissance_mandataire.get()
    mandataire_adresse = entry_adresse_mandataire.get()
    lieu_redaction = entry_lieu_redaction.get()

    # Vérification des champs obligatoires
    if not all([mandant_nom, mandant_prenom, mandant_date_naissance, mandant_lieu_naissance,
                mandant_adresse, mandataire_nom, mandataire_prenom,
                mandataire_date_naissance, mandataire_lieu_naissance, lieu_redaction]):
        messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
        return

    # Détection de la date actuelle
    date_redaction = datetime.today().strftime('%d/%m/%Y')

    # Génération du texte de la procuration
    texte_procuration = f"""
    Je soussigné(e) {mandant_nom} {mandant_prenom}, né(e) le {mandant_date_naissance} à {mandant_lieu_naissance},
    domicilié(e) au {mandant_adresse},
    donne procuration à {mandataire_nom} {mandataire_prenom}, né(e) le {mandataire_date_naissance} à {mandataire_lieu_naissance},
    domicilié(e) au {mandataire_adresse},
    pour récupérer un colis.

    Fait le {date_redaction} à {lieu_redaction}.

    Signature du mandant : ________________________

    Signature du mandataire : _____________________
    """
    # Affichage du résultat
    messagebox.showinfo("Procuration Générée", texte_procuration)
    return texte_procuration

# Fonction pour ajouter le texte au PDF avec gestion des retours à la ligne
def ajouter_texte(canvas, texte, largeur_max):
    y_position = 750  # Position de départ pour le texte (à ajuster en fonction de votre mise en page)
    for ligne in texte.split("\n"):
        # Découper les lignes qui dépassent la largeur maximale
        mots = ligne.split()
        ligne_courante = ""
        for mot in mots:
            # Si ajouter le mot dépasse la largeur maximale, on passe à la ligne suivante
            if canvas.stringWidth(ligne_courante + " " + mot) < largeur_max:
                ligne_courante += " " + mot if ligne_courante else mot
            else:
                canvas.drawString(72, y_position, ligne_courante)
                y_position -= 14  # Décalage de la ligne suivante (ajustez si nécessaire)
                ligne_courante = mot  # Commencer une nouvelle ligne avec le mot
        # Dessiner la dernière ligne
        canvas.drawString(72, y_position, ligne_courante)
        y_position -= 14  # Décalage pour la ligne suivante

# Fonction pour générer le PDF
def telecharger_pdf():
    procuration_texte = generer_procuration()  # Récupération du texte de la procuration

    # Si le texte est vide (cas où l'utilisateur n'a pas rempli les champs), on ne génère pas le PDF
    if not procuration_texte:
        return

    # Ouvrir une boîte de dialogue pour choisir où enregistrer le fichier PDF
    fichier_pdf = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])

    if fichier_pdf:  # Si l'utilisateur a choisi un emplacement de sauvegarde
        # Création du fichier PDF
        c = canvas.Canvas(fichier_pdf, pagesize=letter)
        width, height = letter  # Dimensions de la page

        # Ajouter le texte de la procuration, avec un retour à la ligne si nécessaire
        ajouter_texte(c, procuration_texte, width - 144)  # 72 points de marge de chaque côté

        # Sauvegarde du PDF
        c.save()
        messagebox.showinfo("Succès", "Le fichier PDF a été généré avec succès !")

# Interface graphique (Tkinter)
root = tk.Tk()
root.title("Générateur de Procuration")

# Informations du mandant
tk.Label(root, text="Informations du mandant").pack()
entry_nom_mandant = tk.Entry(root, width=50)
entry_nom_mandant.pack()
entry_nom_mandant.insert(0, "Nom du mandant")

entry_prenom_mandant = tk.Entry(root, width=50)
entry_prenom_mandant.pack()
entry_prenom_mandant.insert(0, "Prénom du mandant")

entry_date_naissance_mandant = tk.Entry(root, width=50)
entry_date_naissance_mandant.pack()
entry_date_naissance_mandant.insert(0, "Date de naissance du mandant (JJ/MM/AAAA)")

entry_lieu_naissance_mandant = tk.Entry(root, width=50)
entry_lieu_naissance_mandant.pack()
entry_lieu_naissance_mandant.insert(0, "Lieu de naissance du mandant")

entry_adresse_mandant = tk.Entry(root, width=50)
entry_adresse_mandant.pack()
entry_adresse_mandant.insert(0, "Adresse complète du mandant")

# Informations du mandataire
tk.Label(root, text="Informations du mandataire").pack()
entry_nom_mandataire = tk.Entry(root, width=50)
entry_nom_mandataire.pack()
entry_nom_mandataire.insert(0, "Nom du mandataire")

entry_prenom_mandataire = tk.Entry(root, width=50)
entry_prenom_mandataire.pack()
entry_prenom_mandataire.insert(0, "Prénom du mandataire")

entry_date_naissance_mandataire = tk.Entry(root, width=50)
entry_date_naissance_mandataire.pack()
entry_date_naissance_mandataire.insert(0, "Date de naissance du mandataire (JJ/MM/AAAA)")

entry_lieu_naissance_mandataire = tk.Entry(root, width=50)
entry_lieu_naissance_mandataire.pack()
entry_lieu_naissance_mandataire.insert(0, "Lieu de naissance du mandataire")

entry_adresse_mandataire = tk.Entry(root, width=50)
entry_adresse_mandataire.pack()
entry_adresse_mandataire.insert(0, "Adresse complète du mandataire")

# Informations de rédaction
tk.Label(root, text="Lieu de rédaction").pack()
entry_lieu_redaction = tk.Entry(root, width=50)
entry_lieu_redaction.pack()
entry_lieu_redaction.insert(0, "Lieu (ville) de rédaction")

# Boutons pour générer la procuration et télécharger le PDF
tk.Button(root, text="Générer la procuration", command=generer_procuration).pack(pady=10)
tk.Button(root, text="Télécharger en PDF", command=telecharger_pdf).pack(pady=10)

# Exécution de l'interface
root.mainloop()
