import { DictionarySearch } from '../components/DictionarySearch';
import { MissList } from '../components/MissList';

export function DictionaryPage() {
  return (
    <div className="container">
      <DictionarySearch />
      <MissList />
    </div>
  );
}