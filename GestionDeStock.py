from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, \
    QTableWidget, QTableWidgetItem, QMessageBox, QHeaderView, QDialog, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys
import mysql.connector
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPalette, QColor


class Product:
    def __init__(self, name, price, quantity, category):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category

class StockManagementGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.stock = []

        # Connexion à la base de données
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="stock"
        )
        self.cursor = self.conn.cursor()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Gestion de stock")
        self.setGeometry(100, 100, 800, 600)

        # Définir les couleurs personnalisées
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(200, 200, 200))  # Couleur de fond de la fenêtre
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))  # Couleur du texte
        palette.setColor(QPalette.Button, QColor(150, 150, 150))  # Couleur des boutons
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))  # Couleur du texte des boutons
        self.setPalette(palette)

        # Définir l'icône de la fenêtre principale
        icon = QIcon("icon1.png")  # Remplacez par le chemin de votre image
        self.setWindowIcon(icon)

        main_layout = QVBoxLayout()

        # Product details
        product_layout = QHBoxLayout()
        product_layout.addWidget(QLabel("Nom:"))
        self.name_entry = QLineEdit()
        product_layout.addWidget(self.name_entry)

        product_layout.addWidget(QLabel("Prix:"))
        self.price_entry = QLineEdit()
        product_layout.addWidget(self.price_entry)

        product_layout.addWidget(QLabel("Quantité:"))
        self.quantity_entry = QLineEdit()
        product_layout.addWidget(self.quantity_entry)

        product_layout.addWidget(QLabel("Catégorie:"))
        self.category_combobox = QComboBox()
        self.category_combobox.addItem("Électronique")
        self.category_combobox.addItem("Vêtements")
        self.category_combobox.addItem("Alimentation")
        product_layout.addWidget(self.category_combobox)

        add_button = QPushButton("Ajouter au stock")
        add_button.clicked.connect(self.add_product)
        product_layout.addWidget(add_button)

        main_layout.addLayout(product_layout)

        # Stock table
        self.stock_table = QTableWidget()
        self.stock_table.setColumnCount(5)
        self.stock_table.setHorizontalHeaderLabels(["Nom", "Prix", "Quantité", "Catégorie", "Prix Total"])
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        main_layout.addWidget(self.stock_table)

        # Options
        self.options_widget = QWidget()
        options_layout = QVBoxLayout()

        # Search product
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Rechercher un produit:"))
        self.search_entry = QLineEdit()
        search_layout.addWidget(self.search_entry)
        search_button = QPushButton("Rechercher")
        search_button.clicked.connect(self.search_product)
        search_button.clicked.connect(self.highlight_row)
        search_layout.addWidget(search_button)
        options_layout.addLayout(search_layout)


        # # Update quantity
        # update_layout = QHBoxLayout()
        # update_layout.addWidget(QLabel("Mettre à jour la quantité:"))
        # self.update_entry = QLineEdit()
        # update_layout.addWidget(self.update_entry)
        # update_quantity_button = QPushButton("Mettre à jour")
        # update_quantity_button.clicked.connect(self.update_quantity)
        # update_layout.addWidget(update_quantity_button)
        # options_layout.addLayout(update_layout)

        # Delete product
        delete_layout = QHBoxLayout()
        delete_layout.addWidget(QLabel("Supprimer un produit:"))
        self.delete_entry = QLineEdit()
        delete_layout.addWidget(self.delete_entry)
        delete_button = QPushButton("Supprimer")
        delete_button.clicked.connect(self.delete_product)
        delete_layout.addWidget(delete_button)
        options_layout.addLayout(delete_layout)

        # Sort stock
        sort_layout = QHBoxLayout()
        sort_layout.addWidget(QLabel("Trier le stock par:"))
        self.sort_combobox = QComboBox()
        self.sort_combobox.addItem("Nom")
        self.sort_combobox.addItem("Prix")
        self.sort_combobox.addItem("Quantité")
        sort_layout.addWidget(self.sort_combobox)
        self.sort_order_combobox = QComboBox()
        self.sort_order_combobox.addItem("Croissant")
        self.sort_order_combobox.addItem("Décroissant")
        sort_layout.addWidget(self.sort_order_combobox)
        sort_button = QPushButton("Trier")
        sort_button.clicked.connect(self.sort_stock)
        sort_layout.addWidget(sort_button)
        options_layout.addLayout(sort_layout)

        # Show statistics
        statistics_button = QPushButton("Statistiques du stock")
        statistics_button.clicked.connect(self.show_statistics)
        options_layout.addWidget(statistics_button)

        self.options_widget.setLayout(options_layout)
        main_layout.addWidget(self.options_widget)

        self.setLayout(main_layout)

        # Show stock
        show_stock_button = QPushButton("Affichage du stock")
        show_stock_button.clicked.connect(self.show_stock)
        options_layout.addWidget(show_stock_button)

        self.options_widget.setLayout(options_layout)
        main_layout.addWidget(self.options_widget)

        self.setLayout(main_layout)



    def add_product(self):
        try:
            name = self.name_entry.text()
            price = float(self.price_entry.text())
            quantity = int(self.quantity_entry.text())
            category = self.category_combobox.currentText()

            product = Product(name, price, quantity, category)
            self.stock.append(product)

            self.update_stock_display()

            self.name_entry.clear()
            self.price_entry.clear()
            self.quantity_entry.clear()

            # Établir la connexion à la base de données
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='stock'
            )
            cursor = connection.cursor()

            # Insérer les données dans la table produit
            query = "INSERT INTO produit (nom, prix, quantite, categorie) VALUES (%s, %s, %s, %s)"
            values = (name, price, quantity, category)
            cursor.execute(query, values)
            connection.commit()

            # Fermer la connexion à la base de données
            cursor.close()
            connection.close()


        except mysql.connector.Error as error:

            QMessageBox.critical(self, "Erreur lors de l'ajout du produit", str(error))


        except ValueError:

            QMessageBox.warning(self, "Erreur de saisie", "Veuillez entrer des valeurs numériques valides pour le prix "

                                                          "et la quantité.")

    def update_stock_display(self):
        self.stock_table.setRowCount(len(self.stock))

        for row, product in enumerate(self.stock):
            self.stock_table.setItem(row, 0, QTableWidgetItem(product.name))
            self.stock_table.setItem(row, 1, QTableWidgetItem(str(product.price)))
            self.stock_table.setItem(row, 2, QTableWidgetItem(str(product.quantity)))
            self.stock_table.setItem(row, 3, QTableWidgetItem(product.category))
            self.stock_table.setItem(row, 4, QTableWidgetItem(str(product.price * product.quantity)))

    def search_product(self):
        search_term = self.search_entry.text()

        results = []
        for row, product in enumerate(self.stock):
            if search_term.lower() in product.name.lower():
                results.append(product)
                self.stock_table.setRowHidden(row, False)  # Afficher la ligne correspondante
                self.highlight_row(row)  # Mettre en évidence la ligne
                #self.clear_search_entry()

            # else:
            #    self.stock_table.setRowHidden(row, True)  # Cacher les autres lignes

        if not results:
            QMessageBox.information(self, "Recherche de produit", "Aucun produit trouvé.")
            self.clear_search_entry()

    def highlight_row(self, row):
        for col in range(self.stock_table.columnCount()):
            item = self.stock_table.item(row, col)
            item.setBackground(Qt.yellow)  # Changer la couleur de fond de la cellule en jaune

    def clear_search_entry(self):
        self.search_entry.clear()
        self.reset_row_colors()

    def reset_row_colors(self):
        for row in range(self.stock_table.rowCount()):
            for col in range(self.stock_table.columnCount()):
                item = self.stock_table.item(row, col)
                item.setBackground(Qt.white)  # Rétablir la couleur de fond par défaut (blanc)

    def update_quantity(self):
        try:
            product_name = self.update_entry.text()
            new_quantity = int(self.quantity_entry.text())

            for product in self.stock:
                if product.name.lower() == product_name.lower():
                    product.quantity = new_quantity
                    self.update_stock_display()
                    self.update_entry.clear()
                    self.quantity_entry.clear()
                    return

            QMessageBox.warning(self, "Mise à jour de la quantité", f"Produit '{product_name}' non trouvé.")

        except ValueError:
            QMessageBox.warning(self, "Erreur de saisie", "Veuillez entrer une valeur numérique valide pour la quantité.")

    def delete_product(self):
        product_name = self.delete_entry.text()

        try:
            # Établir la connexion à la base de données
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='stock'
            )
            cursor = connection.cursor()

            # Exécuter la requête DELETE
            query = "DELETE FROM produit WHERE nom = %s"
            values = (product_name,)
            cursor.execute(query, values)

            # Appliquer les modifications
            connection.commit()

            # Fermer le curseur et la connexion à la base de données
            cursor.close()
            connection.close()

            for product in self.stock:
                if product.name.lower() == product_name.lower():
                    self.stock.remove(product)
                    self.update_stock_display()
                    self.delete_entry.clear()
                    return

            QMessageBox.warning(self, "Suppression du produit", f"Produit '{product_name}' non trouvé.")

        except mysql.connector.Error as error:
            QMessageBox.critical(self, "Erreur lors de la suppression du produit", str(error))

    def sort_stock(self):
        sort_key = self.sort_combobox.currentText()
        sort_order = self.sort_order_combobox.currentText()

        if sort_key == "Nom":
            self.stock.sort(key=lambda product: product.name, reverse=(sort_order == "Décroissant"))
        elif sort_key == "Prix":
            self.stock.sort(key=lambda product: product.price, reverse=(sort_order == "Décroissant"))
        elif sort_key == "Quantité":
            self.stock.sort(key=lambda product: product.quantity, reverse=(sort_order == "Décroissant"))

        self.update_stock_display()

    def show_statistics(self):
        try:
            total_products = len(self.stock)
            total_value = sum([product.price * product.quantity for product in self.stock])
            min_quantity = min([product.quantity for product in self.stock])
            max_quantity = max([product.quantity for product in self.stock])

            QMessageBox.information(self, "Statistiques du stock",
                                    f"Nombre total de produits: {total_products}\n"
                                    f"Valeur totale du stock: {total_value}\n"
                                    f"Quantité minimale: {min_quantity}\n"
                                    f"Quantité maximale: {max_quantity}")

        except ValueError:
            QMessageBox.warning(self, "Erreur de calcul", "Une erreur s'est produite lors du calcul des statistiques.")

    def show_stock(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Stock")
        dialog_layout = QVBoxLayout(dialog)

        stock_table = QTableWidget()
        stock_table.setColumnCount(4)
        stock_table.setHorizontalHeaderLabels(["Nom", "Prix", "Quantité", "Catégorie"])
        stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row, product in enumerate(self.stock):
            stock_table.insertRow(row)
            stock_table.setItem(row, 0, QTableWidgetItem(product.name))
            stock_table.setItem(row, 1, QTableWidgetItem(str(product.price)))
            stock_table.setItem(row, 2, QTableWidgetItem(str(product.quantity)))
            stock_table.setItem(row, 3, QTableWidgetItem(product.category))

        dialog_layout.addWidget(stock_table)

        dialog.setLayout(dialog_layout)
        dialog.exec_()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quitter', 'Êtes-vous sûr de vouloir quitter ?', QMessageBox.Yes,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            # Fermeture de la connexion à la base de données
            self.cursor.close()
            self.conn.close()

            event.accept()
        else:
            event.ignore()



app = QApplication(sys.argv)
window = StockManagementGUI()
window.show()
sys.exit(app.exec_())
